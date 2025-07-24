"""
İşaret dili işlem hattı için integration testler
El algılama -> İşaret tanıma -> Çeviri -> Mors kodu dönüşümü
"""

import unittest

import cv2
import numpy as np

from src.hand_detector import HandDetector
from src.morse_service import MorseCodeService
from src.sign_language_service import SignLanguageService
from src.translator_service import TranslatorService


class TestSignLanguagePipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Tüm testler için bir kere çalışacak hazırlık"""
        cls.hand_detector = HandDetector()
        cls.sign_service = SignLanguageService()
        cls.translator = TranslatorService()

    def setUp(self):
        """Her test öncesi çalışacak hazırlık"""
        # Create artificial image for test (640x480 black image)
        self.test_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_hand_detection(self):
        """El algılama testi"""
        results = self.hand_detector.detect_hands(self.test_frame)
        self.assertIsNotNone(results)

    def test_sign_recognition_no_hand(self):
        """El olmayan görüntüde işaret tanıma testi"""
        frame, letter, stability = self.sign_service.process_frame(self.test_frame)
        self.assertEqual(letter, "")
        self.assertIsNone(stability)

    def test_translation_pipeline(self):
        """Çeviri işlem hattı testi"""
        # English -> Turkish translation
        test_text = "HELLO"
        translated = self.translator.translate(test_text, src_lang="en", dest_lang="tr")
        self.assertIsInstance(translated, str)
        self.assertTrue(len(translated) > 0)

        # Convert translation to morse code
        morse = MorseCodeService.text_to_morse(translated)
        self.assertIsInstance(morse, str)
        self.assertTrue(len(morse) > 0)

    def test_full_pipeline_empty_frame(self):
        """Boş kare için tam işlem hattı testi"""
        # Hand detection and sign recognition
        frame, letter, stability = self.sign_service.process_frame(self.test_frame)
        self.assertEqual(letter, "")

        # Translation (for empty text)
        translated = self.translator.translate("", src_lang="en", dest_lang="tr")
        self.assertEqual(translated, "")

        # Morse code conversion (for empty text)
        morse = MorseCodeService.text_to_morse("")
        self.assertEqual(morse, "")

    def tearDown(self):
        """Her test sonrası temizlik"""
        self.test_frame = None

    @classmethod
    def tearDownClass(cls):
        """Tüm testler bitince çalışacak temizlik"""
        if hasattr(cls.sign_service, "release_resources"):
            cls.sign_service.release_resources()


if __name__ == "__main__":
    unittest.main()
