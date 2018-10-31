import yaml
import logging


class ServiceFactory:

    _config = None
    _config_file_path = "./config/factory.yml"

    def __init__(self):
        try:
            with open(self._config_file_path, 'r') as file:
                self._config = yaml.load(file)
        except Exception as e:
            logging.error("can not read factory config file withe error {}".format(e))

    def get_base_class(self):
        if self._config is None or 'base_class' not in self._config:
            return None
        return self._config['base_class']


