# coding=utf-8
"""
Etcher's Document Library Manager
"""
from pathlib import Path

import elib
from pkg_resources import DistributionNotFound, get_distribution

LOGGER = elib.custom_logging.get_logger('EDLM',)

HERE = Path(__file__).parent.parent.absolute()

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = '"EDLM" package not installed'

LOGGER.info(f'EDLM version {__version__}')
