"""
Sign Language Translator Project
A modular sign language translator application.
"""

import logging
import os


# Logging system
def setup_logging(log_level=logging.INFO, log_file=None):
    """Configures the logging system.

    Args:
        log_level: Logging level (default: INFO)
        log_file: Path to the log file (writes only to console if None)
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handlers = []

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)

    # Add file handler (if specified)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)

    # Root logger configuration
    logging.basicConfig(level=log_level, format=log_format, handlers=handlers)

    logger = logging.getLogger("SignLanguageApp")
    logger.info("Logging system started")


# Package modules
__all__ = [
    "morse_service",
    "hand_detector",
    "sign_language_model",
    "translator_service",
    "sign_language_service",
    "app_state",
    "main_app",
]

# Version info
__version__ = "1.0.0"
