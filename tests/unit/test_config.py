"""
Unit tests for configuration management
"""

import os
import tempfile
import unittest

import yaml

from src.config import Config
from src.exceptions import ConfigurationException


class TestConfig(unittest.TestCase):
    def setUp(self):
        """Setup to run before each test"""
        # Create temporary test file
        self.temp_dir = tempfile.mkdtemp()
        self.test_config_file = os.path.join(self.temp_dir, "test_config.yaml")

    def tearDown(self):
        """Cleanup to run after each test"""
        try:
            if os.path.exists(self.test_config_file):
                os.remove(self.test_config_file)
            os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Cleanup error: {e}")

    def test_default_configuration(self):
        """Default configuration test"""
        config = Config()
        self.assertIsNotNone(config.get("log_level"))
        self.assertIsNotNone(config.get("camera_index"))

    def test_nonexistent_key(self):
        """Nonexistent configuration key test"""
        config = Config()
        self.assertIsNone(config.get("nonexistent_key"))
        self.assertEqual(config.get("nonexistent_key", "default"), "default")

    def test_singleton_instance(self):
        """Singleton instance test"""
        config1 = Config()
        config2 = Config()
        self.assertIs(config1, config2)


if __name__ == "__main__":
    unittest.main()
