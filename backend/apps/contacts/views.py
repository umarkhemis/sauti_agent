from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ContactSearchSerializer
from .models import ContactCache

RELATIONSHIP_TERMS = {
    'lug': {
        'mama': 'mother', 'taata': 'father', 'mwana': 'child',
        'muganda': 'sibling', 'kojja': 'uncle', 'senga': 'aunt',
        'jjajja': 'grandmother', 'ojjajja': 'grandfather',
    },
    'ach': {
        'maa': 'mother', 'baba': 'father', 'latin': 'child',
        'omera': 'brother', 'lamaro': 'sister',
    },
    'nyn': {
        'maama': 'mother', 'taata': 'father', 'omwana': 'child',
        'ow\'omukyara': 'sibling',
    },
    'lso': {
        'maama': 'mother', 'taata': 'father', 'omwana': 'child',
    },
    'lgg': {
        'nyua': 'mother', 'baba': 'father', 'azu': 'child',
    },
    'eng': {
        'mom': 'mother', 'dad': 'father', 'mum': 'mother',
        'brother': 'brother', 'sister': 'sister', 'son': 'son',
        'daughter': 'daughter', 'uncle': 'uncle', 'aunt': 'aunt',
    }
}


def resolve_relationship(name_or_relationship: str, language: str) -> str:
    """Resolve local language relationship terms to English"""
    lang_terms = RELATIONSHIP_TERMS.get(language, {})
    lower = name_or_relationship.lower().strip()
    return lang_terms.get(lower, name_or_relationship)


class ResolveContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        name_or_rel = serializer.validated_data['name_or_relationship']
        language = serializer.validated_data['language']
        session_id = serializer.validated_data.get('session_id', '')

        # Resolve relationship term
        resolved = resolve_relationship(name_or_rel, language)
        relationship = resolved if resolved != name_or_rel else ''

        # Look up cached contacts for session
        contacts_qs = ContactCache.objects.filter(user_session=session_id)
        if relationship:
            contacts_qs = contacts_qs.filter(relationship=relationship)
        else:
            contacts_qs = contacts_qs.filter(contact_name__icontains=name_or_rel)

        contacts = [
            {
                'name': c.contact_name,
                'phone': c.phone_number,
                'relationship': c.relationship,
                'telecom': c.telecom,
            }
            for c in contacts_qs
        ]

        # If no cached contacts, return the resolved name for device lookup
        if not contacts:
            contacts = [{'name': resolved, 'phone': '', 'relationship': relationship, 'telecom': ''}]

        is_ambiguous = len(contacts) > 1

        return Response({'success': True, 'data': {
            'contacts': contacts,
            'is_ambiguous': is_ambiguous,
            'resolved_name': resolved,
        }})
