"""
Sign Language Service
Coordinates sign language detection and translation operations.
"""

import json
import logging
import os
import time
from collections import deque

import cv2
import numpy as np

from src.exceptions import SignLanguageError

# Import our project modules
from src.hand_detector import HandDetector
from src.sign_language_model import SignLanguageModel

logger = logging.getLogger(__name__)


class SignLanguageService:
    """Main service class for sign language operations."""

    def __init__(self, model_path=None, gesture_map_path=None):
        """Initialize service components.

        Args:
            model_path: Sign language model file path (uses default path if None)
            gesture_map_path: Gesture map file path (uses default path if None)
        """
        self.hand_detector = HandDetector()
        self.model_path = model_path or "./sign_language_model/EnglishHandSignModel.p"
        self.english_model = self._initialize_model()

        # Load gesture map
        self.gesture_map_path = gesture_map_path or "./data/gesture_map.json"
        self.gesture_map = self._load_gesture_map()

        # Variables for stability
        self.last_predictions = deque(maxlen=30)  # Store last 30 predictions
        self.required_stable_frames = 20  # Same letter must be detected for 20 frames
        self.stable_threshold = 0.8  # 80% of frames must detect the same letter
        self.min_confidence = 0.7  # Minimum confidence threshold

        logger.info("Sign language service initialized")

    def _load_gesture_map(self):
        """Loads the gesture map."""
        try:
            if not os.path.exists(self.gesture_map_path):
                # Default map
                return {
                    "A": {"landmarks": [(0.4, 0.6), (0.5, 0.7)], "confidence": 0.9},
                    "B": {"landmarks": [(0.3, 0.5), (0.4, 0.6)], "confidence": 0.85},
                    # ... other letters
                }

            with open(self.gesture_map_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Could not load gesture map: {e}")
            return {}

    def process_hand_data(self, hand_data):
        """Processes hand data and determines the most suitable sign.

        Args:
            hand_data: List of hand landmark data

        Returns:
            tuple: (detected sign, confidence value)

        Raises:
            SignLanguageError: When invalid hand data or processing error occurs
        """
        try:
            if not hand_data:
                raise SignLanguageError("Hand data is empty")

            # Confidence check
            confidences = [point.get("confidence", 0) for point in hand_data]
            avg_confidence = sum(confidences) / len(confidences)

            if avg_confidence < self.min_confidence:
                return None, 0.0

            # Find closest sign
            best_match = None
            best_distance = float("inf")
            best_confidence = 0.0

            for gesture, data in self.gesture_map.items():
                distance = self._calculate_distance(hand_data, data["landmarks"])
                if distance < best_distance:
                    best_distance = distance
                    best_match = gesture
                    best_confidence = data["confidence"]

            return best_match, best_confidence

        except Exception as e:
            logger.error(f"Hand data processing error: {str(e)}")
            raise SignLanguageError(f"Hand data could not be processed: {str(e)}")

    def _calculate_distance(self, points1, points2):
        """Calculates Euclidean distance between two point sets.

        Args:
            points1: First point set
            points2: Second point set

        Returns:
            float: Calculated distance
        """
        if len(points1) != len(points2):
            return float("inf")

        total_distance = 0
        for p1, p2 in zip(points1, points2):
            # Get positions of both points
            pos1 = np.array([p1["x"], p1["y"]] if isinstance(p1, dict) else p1)
            pos2 = np.array([p2["x"], p2["y"]] if isinstance(p2, dict) else p2)

            # Calculate Euclidean distance
            distance = np.linalg.norm(pos1 - pos2)
            total_distance += distance

        return total_distance / len(points1)

    def _initialize_model(self):
        """Loads the English ASL model."""
        try:
            return SignLanguageModel(self.model_path)
        except Exception as e:
            logger.error(f"Could not load model: {e}")
            raise

    def process_frame(self, frame):
        """Processes frame to detect hands and predict letters.

        Args:
            frame: Frame to process

        Returns:
            tuple: (processed frame, detected letter, stability value)
        """
        H, W, _ = frame.shape
        results = self.hand_detector.detect_hands(frame)
        letter = ""
        stability_info = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Visualize hand
                self.hand_detector.visualize_hands(frame, hand_landmarks)

                # Extract landmark features
                data_aux, x_, y_ = self.hand_detector.extract_landmarks(hand_landmarks)

                # Determine color based on stability
                color, stability = self._get_stability_color()
                stability_info = stability * 100 if stability is not None else None

                # Draw rectangle around hand
                x1, y1, x2, y2 = self.hand_detector.draw_bounding_box(
                    frame,
                    x_,
                    y_,
                    color,
                    (
                        f"Stability: {int(stability_info)}%"
                        if stability_info is not None
                        else None
                    ),
                )

                # Make letter prediction
                if len(data_aux) == 42:
                    letter = self.english_model.predict(data_aux)

                    # Write letter on screen
                    if letter:
                        cv2.putText(
                            frame,
                            letter,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.3,
                            color,
                            2,
                            cv2.LINE_AA,
                        )

        return frame, letter, stability_info

    def _get_stability_color(self):
        """Returns color and stability value based on stability status.

        Returns:
            tuple: (color, stability value) - color in BGR format
        """
        if not self.last_predictions:
            return (0, 0, 255), None  # Red (initial color)

        from collections import Counter

        letter_counts = Counter(self.last_predictions)
        most_common_letter, count = letter_counts.most_common(1)[0]
        stability = count / len(self.last_predictions)

        # 0.0-0.3: Red, 0.3-0.6: Yellow, 0.6-1.0: Green
        if stability < 0.3:
            return (0, 0, 255), stability  # Red
        elif stability < 0.6:
            return (0, 255, 255), stability  # Yellow
        else:
            return (0, 255, 0), stability  # Green

    def update_prediction(self, letter):
        """Adds a new letter prediction and calculates stability.

        Args:
            letter: Detected letter

        Returns:
            tuple: (most detected letter, stability value, count, is stable)
        """
        if letter:
            self.last_predictions.append(letter)

            if len(self.last_predictions) > 0:
                from collections import Counter

                letter_counts = Counter(self.last_predictions)
                most_common_letter, count = letter_counts.most_common(1)[0]

                stability = count / len(self.last_predictions)
                is_stable = (
                    stability >= self.stable_threshold
                    and count >= self.required_stable_frames
                )

                return most_common_letter, stability, count, is_stable

        return None, 0, 0, False

    def clear_predictions(self):
        """Clears the prediction history."""
        self.last_predictions.clear()
        logger.debug("Prediction history cleared")

    def get_detection_stats(self):
        """Returns detection statistics.

        Returns:
            dict: Detection statistics
        """
        stats = {
            "total_predictions": len(self.last_predictions),
            "stable_threshold": self.stable_threshold,
            "required_stable_frames": self.required_stable_frames,
        }

        if self.last_predictions:
            from collections import Counter

            letter_counts = Counter(self.last_predictions)
            most_common_letter, count = letter_counts.most_common(1)[0]

            stats.update(
                {
                    "most_common_letter": most_common_letter,
                    "most_common_count": count,
                    "stability": count / len(self.last_predictions),
                }
            )

        return stats

    def release_resources(self):
        """Releases all resources."""
        if hasattr(self, "hand_detector"):
            self.hand_detector.release()
        self.last_predictions.clear()
