import base64
import logging
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import HttpResponse

from apps.speech.sunbird_client import SunbirdClient
from apps.intent.intent_engine import IntentEngine
from apps.ussd.ussd_codes import get_ussd_code
from apps.ussd.response_parser import USSDResponseParser
from .dialogue_manager import DialogueManager, FILLER_MESSAGES
from .models import ConversationTurn
from .serializers import ProcessVoiceSerializer, ParseUSSDSerializer

logger = logging.getLogger(__name__)


def _get_or_create_session(session_id: str):
    from apps.users.models import UserSession
    if session_id:
        try:
            return UserSession.objects.get(session_id=session_id, is_active=True)
        except UserSession.DoesNotExist:
            pass
    return UserSession.objects.create(session_id=str(uuid.uuid4()))


def _get_turn_number(session_id: str) -> int:
    return ConversationTurn.objects.filter(session_id=session_id).count() + 1


ACTION_RESPONSES = {
    'make_call': 'I will initiate the call for you.',
    'send_sms': 'I will send the message for you.',
    'read_sms': 'Reading your messages.',
    'mobile_money_balance': 'Checking your mobile money balance.',
    'airtime_balance': 'Checking your airtime balance.',
    'data_balance': 'Checking your data balance.',
    'send_money': 'Preparing to send money.',
    'buy_airtime_self': 'Preparing to buy airtime.',
    'buy_airtime_other': 'Preparing to buy airtime for the recipient.',
    'buy_data': 'Preparing to buy data.',
    'withdraw_money': 'Preparing withdrawal.',
    'pay_merchant': 'Preparing merchant payment.',
    'mini_statement': 'Getting your mini statement.',
    'loan_balance': 'Checking your loan balance.',
    'request_loan': 'Preparing loan request.',
}


class ProcessVoiceCommandView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProcessVoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = serializer.validated_data['audio']
        language = serializer.validated_data['language']
        session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())
        audio_bytes = audio_file.read()

        sunbird = SunbirdClient()

        # Step 1: Transcribe
        transcription = sunbird.transcribe(audio_bytes, language)
        transcribed_text = transcription.get('text', '')

        if not transcribed_text:
            return Response({'success': False, 'error': 'Could not transcribe audio', 'code': 'TRANSCRIPTION_FAILED'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Step 2: Translate to English if needed
        if language != 'eng':
            translation = sunbird.translate(transcribed_text, language, 'eng')
            english_text = translation.get('translated_text', transcribed_text)
        else:
            english_text = transcribed_text

        # Step 3: Classify intent
        engine = IntentEngine()
        intent_result = engine.classify_intent(english_text)

        # Step 4: Process dialogue turn
        dm = DialogueManager()
        dialogue_result = dm.process_turn(session_id, intent_result, transcribed_text, language)

        action = dialogue_result.get('action', 'execute')
        intent = dialogue_result.get('intent', 'unknown')
        entities = dialogue_result.get('entities', {})
        requires_input = action in ('confirm', 'clarify')

        # Step 5: Build response text
        if action in ('confirm', 'clarify'):
            response_text_eng = dialogue_result.get('response_text', '')
            action_taken = None
            ussd_code = None
        else:
            response_text_eng = ACTION_RESPONSES.get(intent, 'I will handle that for you.')
            action_taken = intent
            ussd_code = self._build_ussd_code(intent, entities)

        # Step 6: Translate response if needed
        if language != 'eng' and response_text_eng:
            trans = sunbird.translate(response_text_eng, 'eng', language)
            response_text_local = trans.get('translated_text', response_text_eng)
        else:
            response_text_local = response_text_eng

        # Step 7: TTS
        audio_response = None
        if response_text_local:
            audio_bytes_resp = sunbird.text_to_speech(response_text_local, language)
            if audio_bytes_resp:
                audio_response = base64.b64encode(audio_bytes_resp).decode('utf-8')

        # Log turn
        turn_number = _get_turn_number(session_id)
        ConversationTurn.objects.create(
            session_id=session_id,
            turn_number=turn_number,
            user_input_text=transcribed_text,
            system_response_text=response_text_local,
            intent=intent,
            action_taken=action_taken or '',
        )

        response_data = {
            'response_text': response_text_local,
            'audio_response': audio_response,
            'action_taken': action_taken,
            'requires_input': requires_input,
            'session_id': session_id,
            'intent': intent,
            'entities': entities,
        }

        if ussd_code:
            response_data['ussd_code'] = ussd_code

        return Response({'success': True, 'data': response_data})

    def _build_ussd_code(self, intent: str, entities: dict) -> str:
        """Build USSD code for USSD-based intents"""
        telecom = entities.get('telecom', 'MTN')
        try:
            return get_ussd_code(intent, telecom, entities)
        except Exception as e:
            logger.warning(f"Could not build USSD code for {intent}: {e}")
            return None


class ParseUSSDResponseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ParseUSSDSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        raw_response = serializer.validated_data['raw_response']
        intent = serializer.validated_data['intent']
        language = serializer.validated_data['language']

        parser = USSDResponseParser()
        parsed = parser.parse(raw_response, intent)

        spoken_response_eng = parsed.get('spoken_response', raw_response)

        sunbird = SunbirdClient()
        if language != 'eng':
            trans = sunbird.translate(spoken_response_eng, 'eng', language)
            spoken_response = trans.get('translated_text', spoken_response_eng)
        else:
            spoken_response = spoken_response_eng

        audio_bytes = sunbird.text_to_speech(spoken_response, language)
        audio_response = base64.b64encode(audio_bytes).decode('utf-8') if audio_bytes else None

        return Response({'success': True, 'data': {
            'spoken_response': spoken_response,
            'audio_response': audio_response,
            'success': parsed.get('success', True),
            'data': parsed.get('data', {}),
        }})


class GetFillerAudioView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, language):
        filler_text = FILLER_MESSAGES.get(language, FILLER_MESSAGES['eng'])
        sunbird = SunbirdClient()
        audio_bytes = sunbird.text_to_speech(filler_text, language)

        if not audio_bytes:
            return Response({'success': False, 'error': 'Could not generate filler audio'}, status=status.HTTP_502_BAD_GATEWAY)

        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        return Response({'success': True, 'data': {'audio_response': audio_b64, 'language': language, 'text': filler_text}})
