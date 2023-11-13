from typing import Any, Dict
import json

from exception.no_such_config_exception import NoSuchConfigException

DEFAULT_CONFIG_FILENAME = 'config/config.json'


class ConfigurationWrapper:

    config: Dict = dict()

    @staticmethod
    def load_config_file(filename: str = DEFAULT_CONFIG_FILENAME) -> Dict:
        config_dict: dict = dict()

        with open(filename, 'r') as config_file:
            config_dict = json.load(config_file)

        return config_dict

    @staticmethod
    def reload_config_from_file(filename: str = DEFAULT_CONFIG_FILENAME):
        ConfigurationWrapper.config = ConfigurationWrapper.load_config_file(
            filename)

    @staticmethod
    def get_config(config_name: str) -> Any:
        if not ConfigurationWrapper.config:
            ConfigurationWrapper.reload_config_from_file()

        if not config_name in ConfigurationWrapper.config:
            raise NoSuchConfigException(f'Config {config_name} does not exist')

        return ConfigurationWrapper.config.get(config_name)
