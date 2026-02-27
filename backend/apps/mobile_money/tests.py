from django.test import TestCase
from rest_framework.test import APIClient
from .models import MobileMoneyTransaction


class MobileMoneyTransactionModelTest(TestCase):
    def test_create_transaction(self):
        tx = MobileMoneyTransaction.objects.create(
            session_id='test-session',
            transaction_type='send',
            amount=20000,
            recipient_phone='0772123456',
            telecom='MTN',
        )
        self.assertEqual(tx.status, 'pending')
        self.assertEqual(tx.currency, 'UGX')

    def test_transaction_str(self):
        tx = MobileMoneyTransaction.objects.create(
            session_id='test-session',
            transaction_type='balance',
            amount=0,
            telecom='AIRTEL',
        )
        self.assertIn('balance', str(tx))


class InitiateTransactionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_invalid_telecom(self):
        response = self.client.post('/api/v1/mobile-money/initiate/', {
            'telecom': 'UNKNOWN', 'transaction_type': 'send', 'amount': 1000
        }, format='json')
        self.assertEqual(response.status_code, 400)
