# coding=utf-8

import yaml

import collections

from edlm import MAIN_LOGGER
from edlm.utils import ensure_file_exists

LOGGER = MAIN_LOGGER.getChild(__name__)


def read_settings(settings_file: str) -> dict:
    LOGGER.debug(f'reading setting file: {settings_file}')
    ensure_file_exists(settings_file)
    with open(settings_file) as stream:
        return yaml.load(stream)


def update_settings(source, update):
    for key, value in update.items():
        if isinstance(value, collections.Mapping):
            source[key] = update_settings(source.get(key, {}), value)
        else:
            source[key] = update[key]
    return source
