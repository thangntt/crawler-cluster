import configparser


class ConfigProperties:
    __config = None

    @staticmethod
    def get_config():
        if ConfigProperties.__config is None:
            ConfigProperties.__config = configparser.RawConfigParser()
            ConfigProperties.__config.read('../config/config.properties')
        return ConfigProperties.__config


