import ujson
import os
from common.globalstate import state
from config.abstract_config import AbstractConfig


class ProfilesConfig(AbstractConfig):

    def get_config_file_name(self):
        """
        Get the name of the profiles configuration file.
        Returns:
            The name of the profiles configuration file.
        """
        return "profiles.json"

    def get_default_file_name(self):
        """
        Get the name of the default profiles configuration file.
        Returns:
            The name of the default profiles configuration file.
        """
        return "default_config/profiles.json"

    def validate_config(self, config):
        """
        Validate the profiles configuration.
        Args:
            config: The profiles configuration dictionary.
        Returns:
            True if the configuration is valid, False otherwise.
        """
        required_fields = ["low_heater", "low_fan", "middle_heater", "middle_fan", "high_heater", "high_fan"]
        if not all(field in config for field in required_fields):
            return False

        # Check if all values are integers
        if not all(isinstance(value, int) for value in config.values()):
            return False

        return True

    def load_from_json(self, config):
        """
        Load the profiles configuration from JSON.
        Convert all values to integers.
        Args:
            config: The profiles configuration dictionary.
        Returns:
            The loaded profiles configuration dictionary.
        """
        # Cast everything to int:
        for key, value in config.items():
            config[key] = int(value)
        return config

    def write_config(self, config):
        """
        Write the profiles configuration to a file and update the current profile in the global state.
        If the configuration is not valid, raise a ValueError.
        Args:
            config: The profiles configuration dictionary.
        """
        super(ProfilesConfig, self).write_config(config)
        # Reload config:
        current_profile = state.getState('current_profile')
        state.setCurrentProfile(current_profile)
