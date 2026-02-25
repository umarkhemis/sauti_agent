from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, UserSession


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='pass123', phone_number='0772123456')
        self.assertEqual(user.phone_number, '0772123456')
        self.assertEqual(user.preferred_language, 'eng')
        self.assertFalse(user.onboarding_complete)

    def test_user_str(self):
        user = User.objects.create_user(username='testuser2', password='pass123')
        self.assertEqual(str(user), 'testuser2')


class UserSessionModelTest(TestCase):
    def test_create_session(self):
        session = UserSession.objects.create(session_id='test-session-123', detected_language='lug')
        self.assertTrue(session.is_active)
        self.assertEqual(session.detected_language, 'lug')


class SessionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_session(self):
        response = self.client.post('/api/v1/users/session/', {'language': 'lug'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        self.assertIn('session_id', response.data['data'])

    def test_end_session(self):
        session = UserSession.objects.create(session_id='test-del-session')
        response = self.client.delete(f'/api/v1/users/session/{session.session_id}/')
        self.assertEqual(response.status_code, 200)
        session.refresh_from_db()
        self.assertFalse(session.is_active)
