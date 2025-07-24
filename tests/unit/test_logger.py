"""
Unit tests for log management
"""

import logging
import os
import shutil
import time
import unittest

from src.logger import LogManager, _log_manager, get_log_manager


class TestLogger(unittest.TestCase):
    def setUp(self):
        """Run before each test"""
        self.test_log_dir = "test_logs"
        # Reset global singleton
        global _log_manager
        if _log_manager:
            _log_manager.close()
        _log_manager = None

        # Clean test directory
        if os.path.exists(self.test_log_dir):
            try:
                shutil.rmtree(self.test_log_dir)
            except PermissionError:
                time.sleep(1)  # Wait for files to close
                shutil.rmtree(self.test_log_dir)

    def tearDown(self):
        """Run after each test"""
        # Reset global singleton
        global _log_manager
        if _log_manager:
            _log_manager.close()
        _log_manager = None

        # Clean test directory
        if os.path.exists(self.test_log_dir):
            try:
                shutil.rmtree(self.test_log_dir)
            except PermissionError:
                time.sleep(1)  # Wait for files to close
                shutil.rmtree(self.test_log_dir)

    def test_log_dir_creation(self):
        """Log directory creation test"""
        log_manager = LogManager(self.test_log_dir)
        self.assertTrue(os.path.exists(self.test_log_dir))
        log_manager.close()

    def test_log_file_creation(self):
        """Log file creation test"""
        log_manager = LogManager(self.test_log_dir)
        logger = log_manager.get_logger()

        # Write test messages
        logger.debug("Test debug message")
        logger.info("Test info message")
        logger.error("Test error message")

        # Close handlers
        log_manager.close()

        # Check if files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_log_dir, "debug.log")))
        self.assertTrue(os.path.exists(os.path.join(self.test_log_dir, "info.log")))
        self.assertTrue(os.path.exists(os.path.join(self.test_log_dir, "error.log")))

    def test_log_levels(self):
        """Log levels test"""
        log_manager = LogManager(self.test_log_dir)
        logger = log_manager.get_logger()

        # Test messages
        debug_msg = "Test debug message"
        info_msg = "Test info message"
        error_msg = "Test error message"

        logger.debug(debug_msg)
        logger.info(info_msg)
        logger.error(error_msg)

        # Close handlers
        log_manager.close()

        # Check debug log file
        with open(os.path.join(self.test_log_dir, "debug.log"), "r") as f:
            content = f.read()
            self.assertIn(debug_msg, content)
            self.assertIn(info_msg, content)
            self.assertIn(error_msg, content)

        # Check info log file
        with open(os.path.join(self.test_log_dir, "info.log"), "r") as f:
            content = f.read()
            self.assertNotIn(debug_msg, content)
            self.assertIn(info_msg, content)
            self.assertIn(error_msg, content)

        # Check error log file
        with open(os.path.join(self.test_log_dir, "error.log"), "r") as f:
            content = f.read()
            self.assertNotIn(debug_msg, content)
            self.assertNotIn(info_msg, content)
            self.assertIn(error_msg, content)

    def test_singleton_instance(self):
        """Singleton pattern test"""
        # Get first instance
        log_manager1 = get_log_manager()

        # Get second instance
        log_manager2 = get_log_manager()

        # Check if instances are the same
        self.assertIs(log_manager1, log_manager2)

        # Close handlers
        log_manager1.close()


if __name__ == "__main__":
    unittest.main()
