import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class AirtelMoneyClient:
    """
    Airtel Money Uganda API client.
    Uses Airtel Africa Open API (https://openapi.airtel.africa)
    """

    def __init__(self):
        self.client_id = getattr(settings, 'AIRTEL_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'AIRTEL_CLIENT_SECRET', '')
        self.base_url = getattr(settings, 'AIRTEL_BASE_URL', 'https://openapi.airtel.africa')
        self._token = None

    def get_auth_token(self) -> str:
        """Get OAuth2 token"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/oauth2/token",
                json={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'client_credentials',
                },
                headers={'Content-Type': 'application/json'},
                timeout=30,
            )
            response.raise_for_status()
            token = response.json()['access_token']
            self._token = token
            return token
        except Exception as e:
            logger.error(f"Airtel auth error: {e}")
            return ''

    def request_payment(self, amount: float, currency: str, phone: str, reference: str) -> dict:
        """Initiate a collection payment request"""
        try:
            token = self.get_auth_token()
            payload = {
                'reference': reference,
                'subscriber': {'country': 'UG', 'currency': currency, 'msisdn': phone},
                'transaction': {'amount': amount, 'country': 'UG', 'currency': currency, 'id': reference},
            }
            response = requests.post(
                f"{self.base_url}/merchant/v2/payments/",
                json=payload,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json',
                    'X-Country': 'UG',
                    'X-Currency': currency,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return {
                'status': 'pending',
                'transaction_id': data.get('data', {}).get('transaction', {}).get('id', reference),
            }
        except Exception as e:
            logger.error(f"Airtel request_payment error: {e}")
            return {'status': 'failed', 'error': str(e)}

    def get_transaction_status(self, transaction_id: str) -> dict:
        """Get status of a transaction"""
        try:
            token = self.get_auth_token()
            response = requests.get(
                f"{self.base_url}/standard/v1/payments/{transaction_id}",
                headers={
                    'Authorization': f'Bearer {token}',
                    'X-Country': 'UG',
                    'X-Currency': 'UGX',
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return {
                'status': data.get('data', {}).get('transaction', {}).get('status', 'unknown').lower(),
                'transaction_id': transaction_id,
            }
        except Exception as e:
            logger.error(f"Airtel get_transaction_status error: {e}")
            return {'status': 'failed', 'error': str(e)}
