from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import USSDCodeSerializer, USSDResponseSerializer
from .ussd_codes import get_ussd_code
from .response_parser import USSDResponseParser
from .models import USSDRequest


class BuildUSSDCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = USSDCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        intent = serializer.validated_data['intent']
        telecom = serializer.validated_data['telecom']
        params = serializer.validated_data.get('params', {})

        try:
            ussd_code = get_ussd_code(intent, telecom, params)
            return Response({'success': True, 'data': {
                'ussd_code': ussd_code,
                'telecom': telecom,
                'intent': intent,
            }})
        except ValueError as e:
            return Response({'success': False, 'error': str(e), 'code': 'USSD_BUILD_ERROR'}, status=status.HTTP_400_BAD_REQUEST)


class ParseUSSDResponseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = USSDResponseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        raw_response = serializer.validated_data['raw_response']
        intent = serializer.validated_data['intent']

        parser = USSDResponseParser()
        result = parser.parse(raw_response, intent)

        return Response({'success': True, 'data': result})
