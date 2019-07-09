"""Configuration loader."""

import logging
import sys

import yaml


def config_load(path):
    """
    Load a config file.

    :param path     File path (str)
    """
    try:
        with open(path, mode="r") as handle:
            file_content = handle.read()

        loaded_content = yaml.load(file_content)
        return loaded_content

    except IOError as exc:
        logging.traceback(exc)
        sys.exit(1)
