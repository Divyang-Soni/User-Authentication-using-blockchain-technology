import logging
import importlib
from util import config
from models import factory


class ServiceFactory:

    _factory = None
    _config_file_path = "./config/factory.yml"

    def __init__(self):
        self.__initialize_factory()

    def __initialize_factory(self):
        factory_config = config.Config(file_path=self._config_file_path, config_type="factory")
        self._factory = factory.Factory()
        self._factory.base_class = factory_config.get_section('base_class')
        self._factory.directory = factory_config.get_section('directory')
        self._factory.services = factory_config.get_section('services')

    def get_base_class_name(self):
        return self._factory.base_class

    def get_service_class(self, service, method):
        try:
            service_cfg = self._factory.services[service]
            methods = service_cfg['type']
            if method not in methods:
                return None
            module_instance = importlib.import_module(self._factory.directory+"."+service_cfg['module'])
            service_class = getattr(module_instance, service_cfg['class'])
            return service_class
        except Exception as e:
            logging.error("Error while getting instance of service.\n{}".format(e))
        return None