import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from src.exceptions import HandDetectionError
from src.hand_detector import HandDetector


class TestHandDetector(unittest.TestCase):
    def setUp(self):
        """Setup function to run before each test"""
        self.detector = HandDetector()

    def tearDown(self):
        """Cleanup function to run after each test"""
        if hasattr(self, "detector"):
            self.detector.release()

    @patch("src.hand_detector.mp.solutions.hands.Hands")
    def test_detector_initialization(self, mock_hands):
        """Detector initialization test"""
        detector = HandDetector(min_detection_confidence=0.8)
        mock_hands.assert_called_with(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5,
        )

    def test_process_empty_frame(self):
        """Empty frame processing test"""
        with self.assertRaises(HandDetectionError):
            self.detector.find_hands(None)

    def test_process_invalid_frame(self):
        """Invalid frame processing test"""
        invalid_frame = np.zeros((100, 100), dtype=np.uint8)  # 2D array
        with self.assertRaises(HandDetectionError):
            self.detector.find_hands(invalid_frame)


if __name__ == "__main__":
    unittest.main()
