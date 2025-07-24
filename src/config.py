"""
Configuration Management
Provides YAML-based configuration management.
"""

import logging
import os

import yaml

from src.exceptions import ConfigurationException

logger = logging.getLogger(__name__)


class Config:
    """Singleton class for configuration management."""

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initializes the configuration manager."""
        if self._initialized:
            return

        self._initialized = True
        self._config = {
            # Default configuration
            "log_level": "INFO",
            "camera_index": 0,
            "window_size": {"width": 800, "height": 600},
            "detection": {"confidence_threshold": 0.7, "min_tracking_confidence": 0.5},
        }

        logger.info("Configuration manager started")

    def load_config(self, config_file):
        """Loads configuration from a YAML file.

        Args:
            config_file: Path to the configuration file

        Raises:
            ConfigurationException: File read or YAML parsing error
        """
        try:
            if not os.path.exists(config_file):
                raise ConfigurationException(
                    f"Configuration file not found: {config_file}"
                )

            with open(config_file, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            if config_data:
                self._config.update(config_data)
                logger.info(f"Configuration loaded: {config_file}")

        except yaml.YAMLError as e:
            raise ConfigurationException(f"YAML parsing error: {str(e)}")
        except Exception as e:
            raise ConfigurationException(f"Configuration loading error: {str(e)}")

    def get(self, key, default=None):
        """Returns the configuration value.

        Args:
            key: Configuration key (dot separated)
            default: Default value

        Returns:
            Configuration value or default value
        """
        try:
            value = self._config
            for k in key.split("."):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        """Sets the configuration value.

        Args:
            key: Configuration key (dot separated)
            value: New value
        """
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        logger.debug(f"Configuration updated: {key} = {value}")

    def save_config(self, config_file):
        """Saves the configuration to a YAML file.

        Args:
            config_file: Target file path

        Raises:
            ConfigurationException: File write error
        """
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"Configuration saved: {config_file}")

        except Exception as e:
            raise ConfigurationException(f"Configuration save error: {str(e)}")

    def get_all(self):
        """Returns the entire configuration.

        Returns:
            dict: Configuration dictionary
        """
        return self._config.copy()
