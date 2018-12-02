from util import util


class Config:
    __config_type = None
    __config = None

    def __init__(self,file_path='./config/config.yaml', config_type="server"):
        self.__config_type = config_type
        self.__config = util.parse_config(file_path)

    def get_section(self, section):
        if self.__config and section in self.__config:
            return self.__config[section]
        return None

    def get_config_type(self):
        return self.__config_type
