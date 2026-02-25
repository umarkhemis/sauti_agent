import logging
import time
import json
import openai
from django.conf import settings

logger = logging.getLogger(__name__)

INTENTS = [
    'make_call', 'send_sms', 'read_sms',
    'mobile_money_balance', 'airtime_balance', 'data_balance',
    'send_money', 'buy_airtime_self', 'buy_airtime_other',
    'buy_data', 'withdraw_money', 'pay_merchant',
    'mini_statement', 'loan_balance', 'request_loan',
    'unknown',
]


class IntentEngine:
    """GPT-4o powered intent classification engine"""

    def __init__(self):
        self.api_key = getattr(settings, 'OPENAI_API_KEY', '')

    def classify_intent(self, text: str, context: dict = None) -> dict:
        """
        Classify intent from English text.
        Returns: { intent, entities, confidence, requires_clarification, clarification_question }
        """
        start = time.time()
        try:
            client = openai.OpenAI(api_key=self.api_key)

            prompt = self._build_prompt(text, context or {})
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {'role': 'system', 'content': self._system_prompt()},
                    {'role': 'user', 'content': prompt},
                ],
                temperature=0.1,
                response_format={'type': 'json_object'},
            )
            result = json.loads(response.choices[0].message.content)
            result['processing_time_ms'] = int((time.time() - start) * 1000)
            return result
        except Exception as e:
            logger.error(f"IntentEngine error: {e}")
            return {
                'intent': 'unknown',
                'entities': {},
                'confidence': 0.0,
                'requires_clarification': False,
                'clarification_question': None,
                'error': str(e),
                'processing_time_ms': int((time.time() - start) * 1000),
            }

    def _system_prompt(self) -> str:
        return """You are an intent classification engine for a Ugandan voice assistant.
Classify user requests into these intents:
make_call, send_sms, read_sms, mobile_money_balance, airtime_balance, data_balance,
send_money, buy_airtime_self, buy_airtime_other, buy_data, withdraw_money, pay_merchant,
mini_statement, loan_balance, request_loan, unknown

Extract entities: contact_name, phone_number, amount, telecom (MTN/AIRTEL), recipient_name, message

Respond in JSON format:
{
  "intent": "intent_name",
  "entities": { "key": "value" },
  "confidence": 0.95,
  "requires_clarification": false,
  "clarification_question": null
}

If telecom is unknown for money transfer, set requires_clarification=true and ask which network."""

    def _build_prompt(self, text: str, context: dict) -> str:
        ctx_str = json.dumps(context) if context else '{}'
        return f"User said: \"{text}\"\nContext: {ctx_str}\nClassify the intent."
