from django.test import TestCase
from rest_framework.test import APIClient
from .models import ContactCache
from .views import resolve_relationship


class RelationshipResolutionTest(TestCase):
    def test_luganda_mama(self):
        result = resolve_relationship('mama', 'lug')
        self.assertEqual(result, 'mother')

    def test_acholi_baba(self):
        result = resolve_relationship('baba', 'ach')
        self.assertEqual(result, 'father')

    def test_unknown_name(self):
        result = resolve_relationship('John', 'eng')
        self.assertEqual(result, 'John')


class ContactCacheModelTest(TestCase):
    def test_create_contact(self):
        contact = ContactCache.objects.create(
            user_session='test-session',
            contact_name='Nakato Grace',
            phone_number='0772123456',
            relationship='mother',
        )
        self.assertEqual(str(contact), 'Nakato Grace (0772123456)')


class ResolveContactViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_resolve_contact(self):
        response = self.client.post('/api/v1/contacts/resolve/', {
            'name_or_relationship': 'mama',
            'language': 'lug',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['resolved_name'], 'mother')
