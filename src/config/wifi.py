import ujson
import os

from config.abstract_config import AbstractConfig


class WifiConfig(AbstractConfig):

    def get_config_file_name(self):
        """
        Get the name of the WiFi configuration file.
        Returns:
            The name of the WiFi configuration file.
        """
        return "wifi.json"

    def get_default_file_name(self):
        """
        Get the name of the default WiFi configuration file.
        Returns:
            The name of the default WiFi configuration file.
        """
        return "default_config/wifi.json"

    def validate_config(self, config):
        """
        Validate the WiFi configuration.
        Args:
            config: The WiFi configuration dictionary.
        Returns:
            True if the configuration is valid, False otherwise.
        """
        if "wifi_mode" in config and config["wifi_mode"] not in [0, 1]:
            return False
        if "wifi_name" in config and not isinstance(config["wifi_name"], str):
            return False
        if "wifi_pass" in config and (not isinstance(config["wifi_pass"], str) or len(config["wifi_pass"]) < 8):
            return False
        return True

    def load_from_json(self, config):
        """
        Load the WiFi configuration from JSON.
        Convert the 'wifi_mode' field to an integer if present.
        Args:
            config: The WiFi configuration dictionary.
        Returns:
            The loaded WiFi configuration dictionary.
        """
        if "wifi_mode" in config:
            config["wifi_mode"] = int(config["wifi_mode"])
        return config
