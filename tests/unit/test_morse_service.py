"""
Unit tests for Morse service
"""

import unittest

from src.morse_service import MorseCodeService


class TestMorseCodeService(unittest.TestCase):
    def setUp(self):
        """Setup function to run before each test"""
        self.morse_service = MorseCodeService()

    def test_text_to_morse_single_letter(self):
        """Single letter conversion test"""
        result = MorseCodeService.text_to_morse("A")
        self.assertEqual(result, ".- ")

    def test_text_to_morse_word(self):
        """Word conversion test"""
        result = MorseCodeService.text_to_morse("SOS")
        self.assertEqual(result, "... --- ... ")

    def test_text_to_morse_with_space(self):
        """Text with space conversion test"""
        result = MorseCodeService.text_to_morse("A B")
        self.assertEqual(result, ".- / -... ")

    def test_text_to_morse_turkish_chars(self):
        """Turkish character conversion test"""
        result = MorseCodeService.text_to_morse("ĞÜŞİÖÇ")
        # Test default behavior for Turkish characters
        self.assertTrue(len(result) > 0)

    def test_text_to_morse_empty(self):
        """Empty text conversion test"""
        result = MorseCodeService.text_to_morse("")
        self.assertEqual(result, "")

    def test_text_to_morse_invalid_chars(self):
        """Invalid character conversion test"""
        result = MorseCodeService.text_to_morse("A#B")
        self.assertEqual(result, ".- # -... ")

    def test_text_to_morse_turkish_chars_default_behavior(self):
        """Turkish character conversion test (test default behavior)"""
        result = MorseCodeService.text_to_morse("ĞÜŞİÖÇ")
        # Test default behavior for Turkish characters
        self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()
