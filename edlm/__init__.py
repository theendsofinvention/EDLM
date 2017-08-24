# coding=utf-8
from pkg_resources import get_distribution, DistributionNotFound
import logging

MAIN_LOGGER = logging.getLogger('EDLM')

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = '"convert" package not installed'
