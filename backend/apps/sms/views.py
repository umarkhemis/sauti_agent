import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ComposeSMSSerializer, ReadSMSSerializer
from .models import SMSLog
from apps.speech.sunbird_client import SunbirdClient


class ComposeSMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ComposeSMSSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        dictated_message = data['dictated_message']
        language = data['language']
        recipient_name = data.get('recipient_name', '')
        recipient_phone = data.get('recipient_phone', '')
        session_id = data.get('session_id', '')

        # Translate message to English if needed
        if language != 'eng':
            sunbird = SunbirdClient()
            result = sunbird.translate(dictated_message, language, 'eng')
            message_body = result.get('translated_text', dictated_message)
        else:
            message_body = dictated_message

        SMSLog.objects.create(
            session_id=session_id,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            message_body=message_body,
            direction='sent',
        )

        return Response({'success': True, 'data': {
            'action': 'send_sms',
            'phone_number': recipient_phone,
            'message_body': message_body,
            'recipient_name': recipient_name,
        }})


class ReadSMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ReadSMSSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        sms_content = serializer.validated_data['sms_content']
        sender_name = serializer.validated_data.get('sender_name', '')
        language = serializer.validated_data['language']

        prefix = f"{sender_name} says: " if sender_name else ""
        full_text_eng = f"{prefix}{sms_content}"

        sunbird = SunbirdClient()

        if language != 'eng':
            trans = sunbird.translate(full_text_eng, 'eng', language)
            spoken_response = trans.get('translated_text', full_text_eng)
        else:
            spoken_response = full_text_eng

        audio_bytes = sunbird.text_to_speech(spoken_response, language)
        audio_response = base64.b64encode(audio_bytes).decode('utf-8') if audio_bytes else None

        return Response({'success': True, 'data': {
            'spoken_response': spoken_response,
            'audio_response': audio_response,
        }})
