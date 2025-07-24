"""
Hand Motion Detector
Detects hand movements and extracts features using the MediaPipe library.
"""

import logging

import cv2
import mediapipe as mp
import numpy as np

from src.exceptions import HandDetectionError

logger = logging.getLogger(__name__)


class HandDetector:
    """Class for detecting hand movements."""

    def __init__(
        self,
        static_image_mode=False,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.5,
        max_num_hands=2,
    ):
        """Initializes the detector and loads necessary MediaPipe tools."""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        logger.info("Hand detector initialized")

    def find_hands(self, frame):
        """Performs hand detection on the given frame and returns landmarks.

        Args:
            frame: Image frame to process (numpy array)

        Returns:
            tuple: (success status, list of hand landmarks)

        Raises:
            HandDetectionError: When invalid frame or processing error occurs
        """
        try:
            if frame is None:
                raise HandDetectionError("Cannot process empty frame")

            if not isinstance(frame, np.ndarray) or len(frame.shape) != 3:
                raise HandDetectionError("Invalid frame format")

            # BGR -> RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                return True, results.multi_hand_landmarks
            return False, None

        except Exception as e:
            logger.error(f"Hand detection error: {str(e)}")
            raise HandDetectionError(f"Hand detection failed: {str(e)}")

    def _process_landmarks(self, landmarks, frame_width, frame_height):
        """Processes hand landmarks and returns normalized coordinates.

        Args:
            landmarks: MediaPipe hand landmarks
            frame_width: Frame width
            frame_height: Frame height

        Returns:
            list: Processed and normalized coordinates
        """
        processed_landmarks = []

        for landmark in landmarks.landmark:
            # Convert to pixel coordinates
            px = min(int(landmark.x * frame_width), frame_width - 1)
            py = min(int(landmark.y * frame_height), frame_height - 1)
            pz = landmark.z

            processed_landmarks.append(
                {
                    "x": px,
                    "y": py,
                    "z": pz,
                    "visibility": (
                        landmark.visibility if hasattr(landmark, "visibility") else 1.0
                    ),
                }
            )

        return processed_landmarks

    def detect_hands(self, frame):
        """Performs hand detection on the given frame."""
        # BGR -> RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(frame_rgb)

    def visualize_hands(self, frame, hand_landmarks):
        """Visualizes joint points on the hand."""
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style(),
        )

    def extract_landmarks(self, hand_landmarks):
        """Extracts feature vector from hand landmarks.

        Returns:
            tuple: (feature vector, x coordinates, y coordinates)
        """
        data_aux = []
        x_ = []
        y_ = []

        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            x_.append(x)
            y_.append(y)

        # Calculate normalized coordinates
        for i in range(len(hand_landmarks.landmark)):
            x = hand_landmarks.landmark[i].x
            y = hand_landmarks.landmark[i].y
            data_aux.append(x - min(x_))
            data_aux.append(y - min(y_))

        return data_aux, x_, y_

    def draw_bounding_box(self, frame, x_, y_, color, stability_info=None):
        """Draws a rectangle around the hand.

        Args:
            frame: Frame
            x_: x coordinates
            y_: y coordinates
            color: Rectangle color (BGR)
            stability_info: Optional stability information text
        """
        H, W, _ = frame.shape

        # Draw rectangle around hand
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Keep coordinates within screen bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(W, x2), min(H, y2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Add stability information
        if stability_info:
            cv2.putText(
                frame,
                stability_info,
                (x1, y2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
                cv2.LINE_AA,
            )

        return (x1, y1, x2, y2)  # Return rectangle coordinates

    def release(self):
        """Releases resources."""
        if hasattr(self, "hands"):
            self.hands.close()
