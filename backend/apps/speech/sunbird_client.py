import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class SunbirdClient:
    """Client for Sunbird AI APIs: ASR, TTS, Translation"""

    def __init__(self):
        self.api_key = getattr(settings, 'SUNBIRD_API_KEY', '')
        self.base_url = getattr(settings, 'SUNBIRD_API_URL', 'https://api.sunbird.ai/tasks')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
        }

    def transcribe(self, audio_bytes: bytes, language: str) -> dict:
        """
        Transcribe audio to text using Sunbird ASR.
        Returns: { text: str, confidence: float, language: str }
        """
        try:
            files = {'audio': ('audio.wav', audio_bytes, 'audio/wav')}
            data = {'language': language}
            response = requests.post(
                f'{self.base_url}/asr',
                headers=self.headers,
                files=files,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return {
                'text': result.get('text', ''),
                'confidence': result.get('confidence', 0.0),
                'language': language,
            }
        except Exception as e:
            logger.error(f"Sunbird ASR error: {e}")
            return {'text': '', 'confidence': 0.0, 'language': language, 'error': str(e)}

    def text_to_speech(self, text: str, language: str) -> bytes:
        """
        Convert text to speech using Sunbird TTS.
        Returns: audio bytes (mp3)
        """
        try:
            payload = {'text': text, 'language': language}
            response = requests.post(
                f'{self.base_url}/tts',
                headers={**self.headers, 'Content-Type': 'application/json'},
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Sunbird TTS error: {e}")
            return b''

    def translate(self, text: str, source_language: str, target_language: str) -> dict:
        """
        Translate text using Sunbird Translation.
        Returns: { translated_text: str, source_language: str, target_language: str }
        """
        try:
            payload = {
                'text': text,
                'source_language': source_language,
                'target_language': target_language,
            }
            response = requests.post(
                f'{self.base_url}/translate',
                headers={**self.headers, 'Content-Type': 'application/json'},
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return {
                'translated_text': result.get('translated_text', text),
                'source_language': source_language,
                'target_language': target_language,
            }
        except Exception as e:
            logger.error(f"Sunbird Translation error: {e}")
            return {
                'translated_text': text,
                'source_language': source_language,
                'target_language': target_language,
                'error': str(e)
            }

    def detect_language(self, audio_bytes: bytes) -> dict:
        """
        Detect language by trying all supported languages.
        Returns: { language: str, code: str, text: str, confidence: float }
        """
        from django.conf import settings
        supported = getattr(settings, 'SUPPORTED_LANGUAGES', {
            'lug': 'Luganda', 'ach': 'Acholi', 'nyn': 'Runyankole',
            'lso': 'Lusoga', 'lgg': 'Lugbara', 'eng': 'English'
        })

        best_result = {'language': 'English', 'code': 'eng', 'text': '', 'confidence': 0.0}
        for code, name in supported.items():
            result = self.transcribe(audio_bytes, code)
            if result.get('confidence', 0) > best_result['confidence']:
                best_result = {
                    'language': name,
                    'code': code,
                    'text': result.get('text', ''),
                    'confidence': result.get('confidence', 0.0),
                }
        return best_result
