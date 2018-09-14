# coding=utf-8
"""
Etcher's Document Library Manager
"""
# pylint: disable=invalid-name
import warnings
from pathlib import Path

import elib
from pkg_resources import DistributionNotFound, get_distribution

LOGGER = elib.custom_logging.get_logger('EDLM', log_to_file=True, use_click_handler=True)
elib.custom_logging.set_root_logger(LOGGER)

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
