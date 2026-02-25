from django.test import TestCase
from rest_framework.test import APIClient
from .ussd_codes import get_ussd_code
from .response_parser import USSDResponseParser


class USSDCodesTest(TestCase):
    def test_mtn_balance(self):
        code = get_ussd_code('mobile_money_balance', 'MTN', {})
        self.assertEqual(code, '*165*5#')

    def test_airtel_balance(self):
        code = get_ussd_code('mobile_money_balance', 'AIRTEL', {})
        self.assertEqual(code, '*185*5#')

    def test_mtn_send_money(self):
        code = get_ussd_code('send_money', 'MTN', {'phone_number': '0772123456', 'amount': 20000})
        self.assertEqual(code, '*165*3*0772123456*20000#')

    def test_invalid_telecom(self):
        with self.assertRaises(ValueError):
            get_ussd_code('mobile_money_balance', 'UNKNOWN', {})


class USSDParserTest(TestCase):
    def test_parse_balance(self):
        parser = USSDResponseParser()
        result = parser.parse('Your MoMo balance is UGX 45,230', 'mobile_money_balance')
        self.assertTrue(result['success'])
        self.assertIn('45,230', result['spoken_response'])

    def test_parse_generic(self):
        parser = USSDResponseParser()
        result = parser.parse('Transaction failed', 'unknown')
        self.assertTrue(result['success'])


class BuildUSSDCodeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_build_code(self):
        response = self.client.post('/api/v1/ussd/build-code/', {
            'intent': 'mobile_money_balance', 'telecom': 'MTN'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['ussd_code'], '*165*5#')
