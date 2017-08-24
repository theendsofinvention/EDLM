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

    def __init__(self, miktex_path=None):
        self.miktex_path = miktex_path or MIKTEX_LOCAL_PATH
        self._pdflatex_version = None

    def setup(self) -> bool:
        return all(
            [
                self.download(),
                self.unzip(),
                self._setup_environment(),
            ]
        )

    def change_miktex_path(self, value):
        logging.debug(f'Changing MikTex path to: {value}')
        self.miktex_path = value

    @property
    def _bin_path(self):
        return os.path.join(self.miktex_path, 'texmfs', 'install', 'miktex', 'bin')

    @property
    def pdflatex_path(self) -> str:
        return os.path.join(self._bin_path, 'pdflatex.exe')

    @property
    def mpm_path(self) -> str:
        return os.path.join(self._bin_path, 'mpm.exe')

    @property
    def initexmf_path(self) -> str:
        return os.path.join(self._bin_path, 'initexmf.exe')

    @property
    def pdflatex_version(self) -> typing.Union[None, str]:
        if not os.path.exists(self.pdflatex_path):
            return None
        if self._pdflatex_version is None:
            stdout = do([self.pdflatex_path, '--version'])
            regex_match = self.re_pdflatex_version.match(stdout)
            if not regex_match:
                return None
            self._pdflatex_version = regex_match.group(1)
        return self._pdflatex_version

    def _setup_environment(self) -> bool:
        if os.path.exists(self._bin_path):
            os.environ['PATH'] += os.pathsep + self._bin_path
            return True
        return False

    def download(self) -> bool:
        if not self._local_setup_exists():
            return download(
                url=MIKTEX_URL,
                outfile=MIKTEX_SETUP_FILE,
                hexdigest=MIKTEX_SHA
            )
        logging.info('Local MikTex setup already exists, skipping download')
        return True

    def unzip(self, force: bool = False) -> bool:
        if not self._local_setup_exists():
            return False

        if os.path.exists(self.miktex_path) and not force:
            logging.debug('Miktex found, skipping install')
            return True

        logging.debug('Unzipping MikTex portable installation')
        with zipfile.ZipFile(MIKTEX_SETUP_FILE, compression=zipfile.ZIP_LZMA) as zip_file:
            all_members = zip_file.infolist()
            with click.progressbar(all_members, show_eta=False, label='Unzipping MikTex') as members:
                for member in members:  # type: ignore
                    assert isinstance(member, zipfile.ZipInfo)
                    zip_file.extract(member, path=self.miktex_path)

    def update_mpm_database(self):
        do([self.mpm_path, '--verbose', '--update-db'])

    def setup_initexmf(self):
        do([self.initexmf_path, '--set-config-value', '[MPM]AutoInstall=1'])
        do([self.initexmf_path, '--update-fndb'])

    @staticmethod
    def _remove_local_setup():
        if os.path.exists(MIKTEX_SETUP_FILE):
            os.remove(MIKTEX_SETUP_FILE)

    @staticmethod
    def _local_setup_exists() -> bool:
        if not os.path.exists(MIKTEX_SETUP_FILE):
            logging.debug(f'File does not exist: {MIKTEX_SETUP_FILE}')
            return False
        with open(MIKTEX_SETUP_FILE, 'rb') as setup_file:
            if get_hash(setup_file.read()) != MIKTEX_SHA:
                logging.debug(f'File is corrupted: {MIKTEX_SETUP_FILE}')
                return False
        return True


MIKTEX = MikTex()
