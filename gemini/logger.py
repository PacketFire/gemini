import logging.config
import yaml


def read_config():
    with open('data/logging.yml', 'r') as fh:
        config = yaml.safe_load(fh.read())

    logging.config.dictConfig(config)
