from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient
from .models import IntentLog
from .intent_engine import IntentEngine


class IntentEngineTest(TestCase):
    @patch('apps.intent.intent_engine.openai')
    def test_classify_intent(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"intent": "send_money", "entities": {"amount": 20000}, "confidence": 0.96, "requires_clarification": false, "clarification_question": null}'
        mock_client.chat.completions.create.return_value = mock_response

        engine = IntentEngine()
        result = engine.classify_intent('Send 20000 to John')
        self.assertEqual(result['intent'], 'send_money')
        self.assertEqual(result['confidence'], 0.96)


class ClassifyIntentViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('apps.intent.views.IntentEngine')
    def test_classify_endpoint(self, mock_engine_class):
        mock_engine = MagicMock()
        mock_engine.classify_intent.return_value = {
            'intent': 'make_call', 'entities': {'contact_name': 'John'},
            'confidence': 0.95, 'requires_clarification': False,
            'clarification_question': None, 'processing_time_ms': 100,
        }
        mock_engine_class.return_value = mock_engine

        response = self.client.post('/api/v1/intent/classify/', {'text': 'Call John'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['intent'], 'make_call')

    def test_classify_missing_text(self):
        response = self.client.post('/api/v1/intent/classify/', {}, format='json')
        self.assertEqual(response.status_code, 400)
