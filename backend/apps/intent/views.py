from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ClassifyIntentSerializer
from .intent_engine import IntentEngine
from .models import IntentLog


class ClassifyIntentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClassifyIntentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text']
        context = serializer.validated_data.get('context', {})
        session_id = serializer.validated_data.get('session_id', '')

        engine = IntentEngine()
        result = engine.classify_intent(text, context)

        IntentLog.objects.create(
            session_id=session_id,
            input_text=text,
            detected_intent=result.get('intent', 'unknown'),
            entities=result.get('entities', {}),
            confidence=result.get('confidence', 0.0),
            processing_time_ms=result.get('processing_time_ms', 0),
        )

        return Response({'success': True, 'data': result})
