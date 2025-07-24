import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from src.exceptions import SignLanguageError
from src.sign_language_service import SignLanguageService


class TestSignLanguageService(unittest.TestCase):
    def setUp(self):
        """Setup function to run before each test"""
        self.service = SignLanguageService()

    def tearDown(self):
        """Cleanup function to run after each test"""
        if hasattr(self, "service"):
            self.service.release_resources()

    def test_service_initialization(self):
        """Service initialization test"""
        self.assertIsNotNone(self.service.hand_detector)
        self.assertIsNotNone(self.service.gesture_map)
        self.assertEqual(self.service.min_confidence, 0.7)

    def test_confidence_threshold(self):
        """Confidence threshold tests"""
        # Low confidence hand data
        low_confidence_data = [
            {"x": 50, "y": 50, "z": 0.0, "confidence": 0.3} for i in range(21)
        ]

        gesture, confidence = self.service.process_hand_data(low_confidence_data)
        self.assertIsNone(gesture)
        self.assertEqual(confidence, 0.0)

    def test_invalid_hand_data(self):
        """Invalid hand data test"""
        invalid_data = None
        with self.assertRaises(SignLanguageError):
            self.service.process_hand_data(invalid_data)

        empty_data = []
        with self.assertRaises(SignLanguageError):
            self.service.process_hand_data(empty_data)


if __name__ == "__main__":
    unittest.main()
