"""
Unit tests for exception classes
"""

import unittest

from src.exceptions import (
    HandRecognitionException,
    SignLanguageException,
    CameraException,
    MorseException,
    ConfigurationException,
    YasminBaseException,
)


class TestExceptions(unittest.TestCase):
    def test_base_exception(self):
        """Base exception class test"""
        exc = YasminBaseException()
        self.assertEqual(str(exc), "An error occurred")

        custom_msg = "Custom error message"
        exc = YasminBaseException(custom_msg)
        self.assertEqual(str(exc), custom_msg)

    def test_hand_recognition_exception(self):
        """Hand recognition exception class test"""
        exc = HandRecognitionException()
        self.assertEqual(str(exc), "An error occurred during hand recognition")

        custom_msg = "Custom hand recognition error"
        exc = HandRecognitionException(custom_msg)
        self.assertEqual(str(exc), custom_msg)

    def test_sign_language_exception(self):
        """Sign language exception class test"""
        exc = SignLanguageException()
        self.assertEqual(str(exc), "An error occurred during sign language translation")

        custom_msg = "Custom sign language error"
        exc = SignLanguageException(custom_msg)
        self.assertEqual(str(exc), custom_msg)

    def test_morse_exception(self):
        """Morse code exception class test"""
        exc = MorseException()
        self.assertEqual(str(exc), "An error occurred during Morse code translation")

        custom_msg = "Custom Morse code error"
        exc = MorseException(custom_msg)
        self.assertEqual(str(exc), custom_msg)

    def test_camera_exception(self):
        """Camera exception class test"""
        exc = CameraException()
        self.assertEqual(str(exc), "An error occurred during camera access")

        custom_msg = "Custom camera error"
        exc = CameraException(custom_msg)
        self.assertEqual(str(exc), custom_msg)

    def test_configuration_exception(self):
        """Configuration exception class test"""
        exc = ConfigurationException()
        self.assertEqual(str(exc), "An error occurred while processing configuration file")

        custom_msg = "Custom configuration error"
        exc = ConfigurationException(custom_msg)
        self.assertEqual(str(exc), custom_msg)


if __name__ == "__main__":
    unittest.main()
