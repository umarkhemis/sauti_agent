from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient
from .models import SMSLog


class SMSLogModelTest(TestCase):
    def test_create_sms_log(self):
        log = SMSLog.objects.create(
            session_id='test-session',
            recipient_name='Mary',
            message_body='Hello',
        )
        self.assertEqual(log.direction, 'sent')
        self.assertEqual(log.status, 'pending')


class ComposeSMSViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_compose_english_sms(self):
        response = self.client.post('/api/v1/sms/compose/', {
            'recipient_name': 'Mary',
            'recipient_phone': '0700000001',
            'dictated_message': 'I will come tomorrow',
            'language': 'eng',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['action'], 'send_sms')
        self.assertEqual(response.data['data']['message_body'], 'I will come tomorrow')

    @patch('apps.sms.views.SunbirdClient')
    def test_compose_luganda_sms(self, mock_client):
        mock_sc = MagicMock()
        mock_sc.translate.return_value = {'translated_text': 'I will come tomorrow'}
        mock_client.return_value = mock_sc

        response = self.client.post('/api/v1/sms/compose/', {
            'dictated_message': 'Njijja enkya',
            'language': 'lug',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['message_body'], 'I will come tomorrow')
