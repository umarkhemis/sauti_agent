from django.test import TestCase
from rest_framework.test import APIClient
from .models import CallLog


class CallLogModelTest(TestCase):
    def test_create_call_log(self):
        log = CallLog.objects.create(
            session_id='test-session',
            contact_name='John',
            phone_number='0772123456',
            status='initiated',
        )
        self.assertEqual(log.status, 'initiated')

    def test_call_log_str(self):
        log = CallLog.objects.create(session_id='s1', contact_name='Mary', phone_number='0700000001')
        self.assertIn('Mary', str(log))


class ResolveCallViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_resolve_by_phone(self):
        response = self.client.post('/api/v1/calls/resolve/', {'phone_number': '0772123456'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['action'], 'initiate_call')

    def test_resolve_missing_contact(self):
        response = self.client.post('/api/v1/calls/resolve/', {}, format='json')
        self.assertEqual(response.status_code, 400)
