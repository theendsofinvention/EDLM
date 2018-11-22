# coding=utf-8
"""
Etcher's Document Library Manager
"""
# pylint: disable=invalid-name
import warnings
from pathlib import Path

from pkg_resources import DistributionNotFound, get_distribution

HERE = Path(__file__).parent.parent.absolute()

try:
    __version__ = get_distribution('edlm').version
except DistributionNotFound:  # pragma: no cover
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            from setuptools_scm import get_version

            __version__ = get_version()
    except (ImportError, ModuleNotFoundError, LookupError):
        __version__ = 'not installed'
