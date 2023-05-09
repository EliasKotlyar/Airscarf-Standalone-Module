import ujson
import os

from config.abstract_config import AbstractConfig


class AdvancedConfig(AbstractConfig):

    def get_config_file_name(self):
        """
        Get the name of the advanced configuration file.
        Returns:
            The name of the advanced configuration file.
        """
        return "advanced.json"

    def get_default_file_name(self):
        """
        Get the name of the default advanced configuration file.
        Returns:
            The name of the default advanced configuration file.
        """
        return "default_config/advanced.json"

    def validate_config(self, config):
        """
        Validate the advanced configuration.
        Args:
            config: The advanced configuration dictionary.
        Returns:
            True if the configuration is valid, False otherwise.
        """
        required_fields = [
            "heater_frequency",
            "fan_frequency",
            "monitoring_supply_current",
            "monitoring_heater_current",
            "monitoring_rpm",
            "diagnose_delay_heater_current",
            "diagnose_delay_rpm",
            "diagnose_delay_supply_current"
        ]
        for field in required_fields:
            if field not in config or not isinstance(config[field], (int, float)):
                return False
        return True

    def load_from_json(self, config):
        """
        Load the advanced configuration from JSON.
        Convert specified fields to integers if present.
        Args:
            config: The advanced configuration dictionary.
        Returns:
            The loaded advanced configuration dictionary.
        """
        required_fields = [
            "heater_frequency",
            "fan_frequency",
            "monitoring_supply_current",
            "monitoring_heater_current",
            "monitoring_rpm",
            "diagnose_delay_heater_current",
            "diagnose_delay_rpm",
            "diagnose_delay_supply_current"
        ]
        for fieldname in required_fields:
            if fieldname in config:
                config[fieldname] = int(config[fieldname])
        return config
