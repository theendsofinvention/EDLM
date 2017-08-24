# coding=utf-8

import os

from edlm import MAIN_LOGGER


LOGGER = MAIN_LOGGER.getChild(__name__)


def ensure_file_exists(path: str) -> str:
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if not os.path.isfile(path):
        raise ValueError(f'not a file: {path}')
    return path


def ensure_folder_exists(path: str) -> str:
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if not os.path.isdir(path):
        raise ValueError(f'not a folder: {path}')
    return path


