import yaml
import os
import re
import logging
import pickle

from datetime import datetime, timedelta


LOG_FORMAT = '%(asctime)-15s %(filename)s %(funcName)s line %(lineno)d %(levelname)s:  %(message)s'

# defining the regex pattern that the parser will use to 'implicitely' tag node
pattern = re.compile(r"\${(.*?)\}")


# constructor that the parser will invoke for !envx
def envx_constructor(loader, node):
    value = loader.construct_scalar(node)
    env_var = pattern.match(value).groups()[0]
    return os.environ.get(env_var, '')


# now define a custom tag ( say pathex ) and associate the regex pattern we defined
yaml.add_implicit_resolver("!envx", pattern)


# 'register' the constructor so that the parser will invoke 'envx_constructor' for each node '!pathex'
yaml.add_constructor('!envx', envx_constructor)


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


def get_previous_date(days):
    return str(datetime.strftime(datetime.utcnow() - timedelta(days), "%Y-%m-%d %H:%M:%S"))
