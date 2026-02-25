import re
import logging

logger = logging.getLogger(__name__)


class USSDResponseParser:
    """Parse raw USSD responses into structured data"""

    def parse(self, raw_response: str, intent: str) -> dict:
        """
        Parse USSD response based on intent.
        Returns: { success: bool, spoken_response: str, data: dict }
        """
        try:
            parser = getattr(self, f'_parse_{intent}', self._parse_generic)
            return parser(raw_response)
        except Exception as e:
            logger.error(f"USSD parse error for {intent}: {e}")
            return {
                'success': True,
                'spoken_response': raw_response,
                'data': {},
            }

    def _parse_mobile_money_balance(self, text: str) -> dict:
        amount = self._extract_amount(text)
        spoken = f"Your Mobile Money balance is {self._format_amount(amount)} shillings." if amount else text
        return {'success': True, 'spoken_response': spoken, 'data': {'amount': amount}}

    def _parse_airtime_balance(self, text: str) -> dict:
        amount = self._extract_amount(text)
        spoken = f"Your airtime balance is {self._format_amount(amount)} shillings." if amount else text
        return {'success': True, 'spoken_response': spoken, 'data': {'amount': amount}}

    def _parse_data_balance(self, text: str) -> dict:
        spoken = f"Your data balance: {text}"
        return {'success': True, 'spoken_response': spoken, 'data': {}}

    def _parse_send_money(self, text: str) -> dict:
        success = 'success' in text.lower() or 'confirmed' in text.lower()
        return {'success': success, 'spoken_response': text, 'data': {}}

    def _parse_mini_statement(self, text: str) -> dict:
        return {'success': True, 'spoken_response': f"Your recent transactions: {text}", 'data': {}}

    def _parse_loan_balance(self, text: str) -> dict:
        amount = self._extract_amount(text)
        spoken = f"Your loan balance is {self._format_amount(amount)} shillings." if amount else text
        return {'success': True, 'spoken_response': spoken, 'data': {'amount': amount}}

    def _parse_generic(self, text: str) -> dict:
        return {'success': True, 'spoken_response': text, 'data': {}}

    def _extract_amount(self, text: str):
        match = re.search(r'[\d,]+(?:\.\d+)?', text)
        if match:
            return float(match.group().replace(',', ''))
        return None

    def _format_amount(self, amount) -> str:
        if amount is None:
            return '0'
        return f"{int(amount):,}"
