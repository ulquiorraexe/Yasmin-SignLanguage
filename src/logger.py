"""
Log management module
"""

import logging
import logging.handlers
import os
from datetime import datetime


class LogManager:
    """Log management class"""

    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.logger = None
        self.handlers = []
        self._create_log_dir()
        self._setup_logger()

    def _create_log_dir(self):
        """Create log directory"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _setup_logger(self):
        """Configure the logger"""
        # Clear previous logger
        if self.logger:
            for handler in self.handlers:
                handler.close()
                self.logger.removeHandler(handler)
            self.handlers = []

        # Create main logger
        self.logger = logging.getLogger("YASMIN")
        self.logger.setLevel(logging.DEBUG)

        # Define formats
        detailed_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        simple_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # File handler for error logs
        error_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, "error.log"),
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            delay=True,  # Do not open file immediately
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_format)

        # File handler for info logs
        info_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_dir, "info.log"),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=3,
            delay=True,  # Do not open file immediately
        )
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(simple_format)

        # File handler for debug logs
        debug_handler = logging.handlers.TimedRotatingFileHandler(
            os.path.join(self.log_dir, "debug.log"),
            when="midnight",
            interval=1,
            backupCount=7,
            delay=True,  # Do not open file immediately
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_format)

        # Add handlers to logger
        self.handlers = [error_handler, info_handler, debug_handler]
        for handler in self.handlers:
            self.logger.addHandler(handler)

    def get_logger(self):
        """Return the logger object"""
        return self.logger

    def close(self):
        """Close the handlers"""
        if self.logger:
            for handler in self.handlers:
                handler.flush()
                handler.close()
                self.logger.removeHandler(handler)
            self.handlers = []


# Singleton instance
_log_manager = None


def get_log_manager():
    """Return the singleton log manager instance"""
    global _log_manager
    if _log_manager is None:
        _log_manager = LogManager()
    return _log_manager
