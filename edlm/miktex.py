# coding=utf-8

import logging
import os
import re
import typing
import zipfile

import click

from edlm import MAIN_LOGGER
from edlm.utils import do, download, get_hash

LOGGER = MAIN_LOGGER.getChild(__name__)

MIKTEX_URL = r'http://ctan.space-pro.be/tex-archive/systems/win32/miktex/setup/miktex-portable-2.9.6361.exe'
MIKTEX_SHA = '920ad0381583f843e8ed46f29ef6adb7'
MIKTEX_SETUP_FILE = './miktex_portable_installation.zip'
MIKTEX_LOCAL_PATH = './miktex'


class MikTex:
    re_pdflatex_version = re.compile(r'MiKTeX-pdfTeX ([\d.]+)')

    def __init__(self):
        # do(['mpm', '--verbose', '--update-db'])
        # do(['initexmf', '--set-config-value', '[MPM]AutoInstall=1'])
        # do(['initexmf', '--update-fndb'])
        pass

MIKTEX = MikTex()
