import logging
from django.conf import settings

logger = logging.getLogger(__name__)

FILLER_MESSAGES = {
    'eng': 'I am working on that, please wait a moment.',
    'lug': 'Nkola ku ekyo, linda akamu.',
    'ach': 'Atye ka timo meno, kur manok.',
    'nyn': 'Nkora kuri ekyo, rinda omwanya omuto.',
    'lso': 'Nkola ku ekyo, linda akasera.',
    'lgg': 'Nze ndi ka dria meni, dria kinoga.',
}

CONFIRMATION_TEMPLATES = {
    'eng': 'You want to {action}. Is that correct?',
    'lug': 'Oyagala {action}. Kituufu?',
    'ach': 'Imito {action}. Mito onyo?',
    'nyn': 'Oyagala {action}. Ni kuri ko?',
    'lso': 'Oyagala {action}. Nkakasa?',
    'lgg': 'Nia {action}. Drini?',
}

INTENTS_REQUIRING_CONFIRMATION = {
    'send_money', 'buy_airtime_self', 'buy_airtime_other',
    'buy_data', 'withdraw_money', 'pay_merchant', 'request_loan',
}


class DialogueManager:
    """Manages conversation state and turn logic"""

    def process_turn(self, session_id: str, intent_result: dict, raw_text: str, language: str = 'eng') -> dict:
        """
        Process a conversation turn.
        Returns: { action: "execute"|"confirm"|"clarify"|"respond", response_text, ... }
        """
        intent = intent_result.get('intent', 'unknown')
        requires_clarification = intent_result.get('requires_clarification', False)
        clarification_question = intent_result.get('clarification_question')

        if requires_clarification and clarification_question:
            return {
                'action': 'clarify',
                'response_text': clarification_question,
                'intent': intent,
                'entities': intent_result.get('entities', {}),
            }

        if intent in INTENTS_REQUIRING_CONFIRMATION:
            confirmation_text = self._build_confirmation(intent, intent_result.get('entities', {}), language)
            return {
                'action': 'confirm',
                'response_text': confirmation_text,
                'intent': intent,
                'entities': intent_result.get('entities', {}),
            }

        return {
            'action': 'execute',
            'response_text': '',
            'intent': intent,
            'entities': intent_result.get('entities', {}),
        }

    def _build_confirmation(self, intent: str, entities: dict, language: str) -> str:
        action_descriptions = {
            'send_money': f"send {entities.get('amount', '?')} shillings to {entities.get('contact_name', '?')}",
            'buy_airtime_self': f"buy {entities.get('amount', '?')} shillings airtime for yourself",
            'buy_airtime_other': f"buy airtime for {entities.get('contact_name', '?')}",
            'buy_data': f"buy data bundle for {entities.get('amount', '?')} shillings",
            'withdraw_money': f"withdraw {entities.get('amount', '?')} shillings",
            'pay_merchant': f"pay merchant {entities.get('merchant_code', '?')}",
            'request_loan': 'request a mobile money loan',
        }
        action_desc = action_descriptions.get(intent, intent)
        template = CONFIRMATION_TEMPLATES.get(language, CONFIRMATION_TEMPLATES['eng'])
        return template.format(action=action_desc)

    def get_filler_message(self, language: str) -> str:
        return FILLER_MESSAGES.get(language, FILLER_MESSAGES['eng'])
