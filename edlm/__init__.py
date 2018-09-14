# coding=utf-8
"""
Etcher's Document Library Manager
"""
import logging
# pylint: disable=invalid-name
import sys
import warnings
from pathlib import Path

from pkg_resources import DistributionNotFound, get_distribution


def _setup_logging():
    format_str = '%(relativeCreated)10d ms ' \
                 '%(levelname)8s ' \
                 '[%(pathname)s@%(lineno)d %(funcName)s]: ' \
                 '%(message)s'
    formatter = logging.Formatter(format_str)
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(formatter)
    _console_handler.setLevel(logging.DEBUG)
    _file_handler = logging.FileHandler('edlm.log', mode='w', encoding='utf8')
    _file_handler.setFormatter(formatter)
    _file_handler.setLevel(logging.DEBUG)
    LOGGER.setLevel(logging.DEBUG)


LOGGER = logging.getLogger('EDLM')
_setup_logging()

HERE = Path(__file__).parent.parent.absolute()

try:
    __version__ = get_distribution('edlm').version
except DistributionNotFound:  # pragma: no cover
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            from setuptools_scm import get_version

            __version__ = get_version()
    except (ImportError, ModuleNotFoundError):
        __version__ = 'not installed'
