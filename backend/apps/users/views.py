from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, UserSession
from .serializers import UserSerializer, UserSessionSerializer
import uuid


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'success': True, 'data': serializer.data})

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SessionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_id = request.data.get('session_id')
        if session_id:
            try:
                session = UserSession.objects.get(session_id=session_id, is_active=True)
                serializer = UserSessionSerializer(session)
                return Response({'success': True, 'data': serializer.data})
            except UserSession.DoesNotExist:
                pass
        session = UserSession.objects.create(
            session_id=str(uuid.uuid4()),
            detected_language=request.data.get('language', 'eng'),
        )
        serializer = UserSessionSerializer(session)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, session_id):
        try:
            session = UserSession.objects.get(session_id=session_id)
            session.is_active = False
            session.save()
            return Response({'success': True, 'message': 'Session ended'})
        except UserSession.DoesNotExist:
            return Response({'success': False, 'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
