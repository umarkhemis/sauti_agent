from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient
from io import BytesIO
from .models import VoiceRequest
from .sunbird_client import SunbirdClient


class SunbirdClientTest(TestCase):
    @patch('apps.speech.sunbird_client.requests.post')
    def test_transcribe(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'text': 'Hello world', 'confidence': 0.95}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = SunbirdClient()
        result = client.transcribe(b'fake-audio', 'eng')
        self.assertEqual(result['text'], 'Hello world')
        self.assertEqual(result['confidence'], 0.95)

    @patch('apps.speech.sunbird_client.requests.post')
    def test_translate(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'translated_text': 'Oli otya'}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = SunbirdClient()
        result = client.translate('How are you', 'eng', 'lug')
        self.assertEqual(result['translated_text'], 'Oli otya')


class TranscribeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('apps.speech.views.SunbirdClient')
    def test_transcribe_endpoint(self, mock_client_class):
        mock_client = MagicMock()
        mock_client.transcribe.return_value = {'text': 'Test text', 'confidence': 0.9, 'language': 'eng'}
        mock_client_class.return_value = mock_client

        audio = BytesIO(b'fake audio data')
        response = self.client.post('/api/v1/speech/transcribe/', {'audio': audio, 'language': 'eng'}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
