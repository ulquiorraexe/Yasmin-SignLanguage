"""
Translation Service
Translates texts into different languages using the Google Translate API.
"""

import logging

from googletrans import Translator

logger = logging.getLogger(__name__)


class TranslatorService:
    """Service class for translation operations."""

    def __init__(self):
        """Initializes the translation service."""
        try:
            self.translator = Translator()
            logger.info("Translation service started")
        except Exception as e:
            logger.error(f"Translation service could not be started: {e}")
            raise

    def translate(self, text, src_lang="tr", dest_lang="en"):
        """Translates text from one language to another.

        Args:
            text: Text to translate
            src_lang: Source language code (default: tr)
            dest_lang: Target language code (default: en)

        Returns:
            str: Translated text
        """
        if not text.strip():
            return ""

        try:
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)

            logger.debug(f"Translation: '{text}' -> '{translated.text}'")
            return translated.text
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"Translation error: {e}"

    def get_available_languages(self):
        """Returns the list of available languages.

        Returns:
            dict: Language code -> Language name mapping
        """
        try:
            # Languages supported by Googletrans
            return self.translator.LANGUAGES
        except Exception as e:
            logger.error(f"Could not get language list: {e}")
            return {}
