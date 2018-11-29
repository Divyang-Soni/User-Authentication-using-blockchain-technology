import yaml
import logging
import pickle
from datetime import datetime


LOG_FORMAT = '%(asctime)-15s %(filename)s %(funcName)s line %(lineno)d %(levelname)s:  %(message)s'


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


def json_to_model(json, obj):
    if not obj:
        return json
    keys = json.keys()
    for key in keys:
        if hasattr(obj, key):
            setattr(obj, key, json[key])
        else:
            return json
    return obj


def model_to_json(obj):
    if obj:
        return pickle.dumps(obj)
    return {}


def init_logging(file_path=None):
    if file_path:
        file_path = "./logs_{}/{}".format(datetime.now(), file_path)
    logging.basicConfig(format=LOG_FORMAT, level="INFO", filename=file_path)
    return logging.getLogger()