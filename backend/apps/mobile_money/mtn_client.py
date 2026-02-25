import uuid
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class MTNMoMoClient:
    """
    MTN Mobile Money Uganda API client.
    Uses MTN MoMo API (https://momodeveloper.mtn.com)
    """

    def __init__(self):
        self.api_user = getattr(settings, 'MTN_MOMO_API_USER', '')
        self.api_key = getattr(settings, 'MTN_MOMO_API_KEY', '')
        self.subscription_key = getattr(settings, 'MTN_MOMO_SUBSCRIPTION_KEY', '')
        self.base_url = getattr(settings, 'MTN_MOMO_BASE_URL', 'https://sandbox.momodeveloper.mtn.com')
        self._token = None

    def _get_auth_token(self) -> str:
        import base64
        credentials = base64.b64encode(f"{self.api_user}:{self.api_key}".encode()).decode()
        response = requests.post(
            f"{self.base_url}/collection/token/",
            headers={
                'Authorization': f'Basic {credentials}',
                'Ocp-Apim-Subscription-Key': self.subscription_key,
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['access_token']

    def request_to_pay(self, amount: float, currency: str, phone: str, reference: str, note: str) -> dict:
        """Initiate a Request to Pay (STK Push equivalent)"""
        try:
            token = self._get_auth_token()
            reference_id = str(uuid.uuid4())
            payload = {
                'amount': str(amount),
                'currency': currency,
                'externalId': reference,
                'payer': {'partyIdType': 'MSISDN', 'partyId': phone},
                'payerMessage': note,
                'payeeNote': note,
            }
            response = requests.post(
                f"{self.base_url}/collection/v1_0/requesttopay",
                json=payload,
                headers={
                    'Authorization': f'Bearer {token}',
                    'X-Reference-Id': reference_id,
                    'X-Target-Environment': 'sandbox',
                    'Ocp-Apim-Subscription-Key': self.subscription_key,
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
            response.raise_for_status()
            return {'status': 'pending', 'reference_id': reference_id}
        except Exception as e:
            logger.error(f"MTN request_to_pay error: {e}")
            return {'status': 'failed', 'error': str(e)}

    def get_transaction_status(self, reference_id: str) -> dict:
        """Get the status of a transaction"""
        try:
            token = self._get_auth_token()
            response = requests.get(
                f"{self.base_url}/collection/v1_0/requesttopay/{reference_id}",
                headers={
                    'Authorization': f'Bearer {token}',
                    'X-Target-Environment': 'sandbox',
                    'Ocp-Apim-Subscription-Key': self.subscription_key,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return {
                'status': data.get('status', 'unknown').lower(),
                'reference_id': reference_id,
                'amount': data.get('amount'),
                'currency': data.get('currency'),
            }
        except Exception as e:
            logger.error(f"MTN get_transaction_status error: {e}")
            return {'status': 'failed', 'error': str(e)}

    def get_account_balance(self) -> dict:
        """Get account balance"""
        try:
            token = self._get_auth_token()
            response = requests.get(
                f"{self.base_url}/collection/v1_0/account/balance",
                headers={
                    'Authorization': f'Bearer {token}',
                    'X-Target-Environment': 'sandbox',
                    'Ocp-Apim-Subscription-Key': self.subscription_key,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return {'balance': data.get('availableBalance'), 'currency': data.get('currency')}
        except Exception as e:
            logger.error(f"MTN get_account_balance error: {e}")
            return {'balance': None, 'error': str(e)}
