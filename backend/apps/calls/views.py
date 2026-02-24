from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ResolveCallSerializer, LogCallSerializer
from .models import CallLog


class ResolveCallView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResolveCallSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data.get('phone_number', '')
        contact_name = serializer.validated_data.get('contact_name', '')

        # Contact lookup is done on device; backend returns action instruction
        if not phone_number and not contact_name:
            return Response({'success': False, 'error': 'phone_number or contact_name required', 'code': 'MISSING_CONTACT'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True, 'data': {
            'action': 'initiate_call',
            'phone_number': phone_number,
            'contact_name': contact_name,
        }})


class LogCallView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogCallSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        call_log = serializer.save()
        return Response({'success': True, 'data': {'id': call_log.id, 'status': call_log.status}}, status=status.HTTP_201_CREATED)
