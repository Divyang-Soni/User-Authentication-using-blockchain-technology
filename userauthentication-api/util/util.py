import yaml
import logging


def parse_config(path="./config/config.yaml"):
    """
    parses yaml
    :param path: config path (default = ./config/config.yaml)
    :return: parsed config dict
    """
    try:
        with open(path, 'r') as ymlfile:
            config = yaml.load(ymlfile)
        return config
    except Exception as e:
        logging.error("Error while parsing config.\n{}".format(e))