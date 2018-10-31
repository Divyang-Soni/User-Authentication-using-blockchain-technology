import yaml
import logging
import importlib

class ServiceFactory:

    _config = None
    _config_file_path = "./config/factory.yml"

    def __init__(self):
        try:
            with open(self._config_file_path, 'r') as file:
                self._config = yaml.load(file)
        except Exception as e:
            logging.error("can not read factory config file withe error {}".format(e))

    def get_base_class_name(self):
        if self._config is None or 'base_class' not in self._config:
            return None
        return self._config['base_class']

    def get_instance(self, service, method):
        try:
            if 'services' not in self._config or service not in self._config['services']:
                return None

            service_cfg = self._config['services'][service]
            methods = service_cfg['type']
            if method not in methods:
                return None

            module = importlib.import_module(self._config['directory']+"."+service_cfg['module'])
            service_instance = getattr(module, service_cfg['class'])
            return service_instance()
        except Exception as e:
            logging.error("Error while getting instance of service.")
        return None