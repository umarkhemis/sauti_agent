from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient
from io import BytesIO
from .models import ConversationTurn
from .dialogue_manager import DialogueManager


class DialogueManagerTest(TestCase):
    def test_execute_simple_intent(self):
        dm = DialogueManager()
        result = dm.process_turn('session-1', {
            'intent': 'airtime_balance',
            'entities': {},
            'confidence': 0.9,
            'requires_clarification': False,
        }, 'Check my airtime', 'eng')
        self.assertEqual(result['action'], 'execute')
        self.assertEqual(result['intent'], 'airtime_balance')

    def test_confirm_send_money(self):
        dm = DialogueManager()
        result = dm.process_turn('session-1', {
            'intent': 'send_money',
            'entities': {'amount': 20000, 'contact_name': 'John'},
            'confidence': 0.95,
            'requires_clarification': False,
        }, 'Send 20000 to John', 'eng')
        self.assertEqual(result['action'], 'confirm')

    def test_clarify_when_needed(self):
        dm = DialogueManager()
        result = dm.process_turn('session-1', {
            'intent': 'send_money',
            'entities': {},
            'confidence': 0.8,
            'requires_clarification': True,
            'clarification_question': 'Which network?',
        }, 'Send money to John', 'eng')
        self.assertEqual(result['action'], 'clarify')


class ProcessVoiceCommandViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('apps.dialogue.views.SunbirdClient')
    @patch('apps.dialogue.views.IntentEngine')
    def test_process_voice_command(self, mock_intent, mock_sunbird):
        mock_sc = MagicMock()
        mock_sc.transcribe.return_value = {'text': 'Check my balance', 'confidence': 0.9, 'language': 'eng'}
        mock_sc.text_to_speech.return_value = b'audio'
        mock_sunbird.return_value = mock_sc

        mock_ie = MagicMock()
        mock_ie.classify_intent.return_value = {
            'intent': 'airtime_balance', 'entities': {},
            'confidence': 0.9, 'requires_clarification': False,
            'clarification_question': None,
        }
        mock_intent.return_value = mock_ie

        audio = BytesIO(b'fake audio')
        response = self.client.post('/api/v1/dialogue/process/', {'audio': audio, 'language': 'eng'}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
