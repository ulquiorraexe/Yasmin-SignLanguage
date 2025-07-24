"""
Sign Language Recognition Model
Recognizes sign language alphabet using a pre-trained model.
"""

import logging
import pickle

import numpy as np

logger = logging.getLogger(__name__)


class SignLanguageModel:
    """Sign language recognition model class."""

    def __init__(self, model_path, labels_dict=None):
        """Loads the model and sets up labels."""
        self.model = self._load_model(model_path)
        self.labels_dict = labels_dict or self._get_default_labels()
        logger.info(f"Sign language model loaded: {model_path}")

    def _load_model(self, model_path):
        """Loads a model saved as pickle."""
        try:
            model_dict = pickle.load(open(model_path, "rb"))
            return model_dict["model"]
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            raise

    def _get_default_labels(self):
        """Returns default English ASL labels."""
        return {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H",
            8: "I",
            9: "J",
            10: "K",
            11: "L",
            12: "M",
            13: "N",
            14: "O",
            15: "P",
            16: "Q",
            17: "R",
            18: "S",
            19: "T",
            20: "U",
            21: "V",
            22: "W",
            23: "X",
            24: "Y",
            25: "Z",
        }

    def predict(self, features):
        """Makes letter prediction based on feature vector.

        Args:
            features: Feature vector (hand landmark coordinates)

        Returns:
            str: Predicted letter or None (in case of failed prediction)
        """
        if len(features) != 42:  # MediaPipe hands 21 landmark (x, y)
            logger.warning(f"Invalid feature vector length: {len(features)}")
            return None

        try:
            prediction = self.model.predict([np.asarray(features)])
            predicted_class = int(prediction[0])
            return self.labels_dict.get(predicted_class)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return None

    def predict_with_confidence(self, features):
        """Returns prediction and confidence value.

        Note: Current model may not provide confidence value, in which case only prediction is returned.

        Returns:
            tuple: (predicted letter, confidence value)
        """
        letter = self.predict(features)
        confidence = 1.0  # Default confidence (if real model doesn't support it)

        # Confidence calculation for future models can be added here

        return letter, confidence
