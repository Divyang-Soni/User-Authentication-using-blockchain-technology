import yaml


def parse_config(path="./config/config.yaml"):
    with open(path, 'r') as ymlfile:
        config = yaml.load(ymlfile)
    return config