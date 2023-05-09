import ujson
import os
from lib.microdot_asyncio import Microdot
from common.globalstate import state

class AbstractConfig:

    def validate_config(self, config):
        """
        Abstract method to validate the configuration.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def get_config_file_name(self):
        """
        Abstract method to get the configuration file name.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def get_default_file_name(self):
        """
        Abstract method to get the default file name.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def load_from_json(self, config):
        """
        Abstract method to load configuration from JSON.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def write_config(self, config):
        """
        Write the configuration to a file.
        If the configuration is not valid, raise a ValueError.
        Set the configuration values in the global state object.
        """
        if not self.validate_config(config):
            raise ValueError("Invalid configuration format")

        for key, value in config.items():
            state.setState(key, value)

        with open(self.get_config_file_name(), "w") as f:
            json = ujson.dumps(config)
            f.write(json)

    def read_config(self):
        """
        Read the configuration from a file.
        If the configuration file does not exist, replace it with the default configuration file.
        If the configuration is not valid, raise a ValueError.
        Return the loaded configuration.
        """
        # If Config does not exist
        if not self.get_config_file_name() in os.listdir():
            self._replace_with_default_config()
        with open(self.get_config_file_name(), "r") as f:
            try:
                config = ujson.load(f)
                self.validate_config(config)
            except ValueError:
                self._replace_with_default_config()
                raise ValueError("Invalid configuration format")
        return config

    def _replace_with_default_config(self):
        """
        Replace the current configuration file with the default configuration file.
        """
        if self.get_config_file_name() in os.listdir():
            os.remove(self.get_config_file_name())

        os.rename(self.get_default_file_name(), self.get_config_file_name())

    def get_microdot_config(self):
        """
        Get the Microdot configuration for handling HTTP requests.
        Define the '/setData' endpoint to receive configuration data and update the configuration file.
        Define the '/data.json' endpoint to retrieve the current configuration.
        Return the Microdot instance with the defined endpoints.
        """
        api_data = Microdot()

        @api_data.post('/setData')
        def setData(request):
            data = request.json
            config = self.load_from_json(data)
            self.write_config(config)
            return {'success': True}

        @api_data.get('/data.json')
        def setData(request):
            return self.read_config()

        return api_data
