import os
from django.core.management.base import BaseCommand
from django.conf import settings


WELCOME_MESSAGES = {
    'welcome_english': ('To use English, start speaking in English', 'eng'),
    'welcome_luganda': ('Okwogera Luganda, yambaza mu Luganda', 'lug'),
    'welcome_runyankole': ('Okukozesa Runyankole, wogerere mu Runyankole', 'nyn'),
    'welcome_acholi': ('Ting lok Acholi, lok ki Acholi', 'ach'),
    'welcome_lusoga': ('Okukozesa Lusoga, yogera mu Lusoga', 'lso'),
    'welcome_lugbara': ('Nze SautiAgent, yaka mu Lugbara', 'lgg'),
}


class Command(BaseCommand):
    help = 'Generate welcome audio files for all supported languages'

    def handle(self, *args, **options):
        from apps.speech.sunbird_client import SunbirdClient
        client = SunbirdClient()

        audio_dir = os.path.join(settings.BASE_DIR, 'assets', 'audio', 'welcome')
        os.makedirs(audio_dir, exist_ok=True)

        for key, (text, language) in WELCOME_MESSAGES.items():
            self.stdout.write(f'Generating {key} ({language})...')
            audio_bytes = client.text_to_speech(text, language)
            if audio_bytes:
                filepath = os.path.join(audio_dir, f'{key}.mp3')
                with open(filepath, 'wb') as f:
                    f.write(audio_bytes)
                self.stdout.write(self.style.SUCCESS(f'Saved {filepath}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to generate {key}'))
