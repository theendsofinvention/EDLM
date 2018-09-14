# coding=utf-8
"""
Base class for external tools
"""
import functools
import os
import sys
import typing
from pathlib import Path

import elib
import elib_run
import pyunpack

from edlm import LOGGER

LOGGER = LOGGER

StrOrPath = typing.Union[str, Path]


@functools.lru_cache(1)
def _find_patool(path=sys.executable) -> Path:
    LOGGER.debug('looking for Patool')
    python_exe = Path(path).absolute()
    LOGGER.debug('python_exe: %s', python_exe)
    patool_path = Path(python_exe.parent, 'patool')
    LOGGER.debug('looking at: %s', patool_path)
    if patool_path.exists():
        LOGGER.debug('patool found: %s', patool_path)
        return patool_path.absolute()

    scripts_path = Path(python_exe.parent, 'scripts')
    if scripts_path.exists() and scripts_path.is_dir():
        patool_path = Path(scripts_path, 'patool')
        LOGGER.debug('looking at: %s', patool_path)
        if patool_path.exists():
            LOGGER.debug('patool found: %s', patool_path)
            return patool_path.absolute()

    raise FileNotFoundError('patool not found')


class BaseExternalTool:
    """
    Base class for external tools
    """
    url = None
    hash = None
    default_archive = None
    default_install = None
    expected_version = None

    def __init__(self, archive: StrOrPath = None, install_dir: StrOrPath = None):
        self.__check_values()

        if archive is None:
            archive = self.default_archive
        if install_dir is None:
            install_dir = self.default_install

        self.archive = elib.path.ensure_file(archive, must_exist=False).absolute()
        self.install_dir = elib.path.ensure_dir(install_dir, must_exist=False).absolute()

        LOGGER.debug('%s: archive: %s', self.__class__.__name__, self.archive)
        LOGGER.debug('%s: install dir: %s', self.__class__.__name__, self.install_dir)

        self._exe = None
        self._version = None

    def __call__(self, cmd: str):
        out, _ = elib_run.run(str(self.get_exe().absolute()) + ' ' + cmd, mute=True)
        return out

    def __check_values(self):
        for value, name in (
                (self.default_install, 'default_install'),
                (self.default_archive, 'default_archive'),
                (self.url, 'url'),
                (self.hash, 'hash'),
                (self.expected_version, 'expected_version'),
        ):
            if value is None:
                raise ValueError(
                    f'Class "{self.__class__.__name__}(BaseExternalTool)" is missing default value for "{name}"')

    def _archive_exists(self) -> bool:  # pragma: no cover
        return self.archive.exists()

    def _archive_is_correct(self) -> bool:
        if not self._archive_exists():
            return False
        return elib.hash_.get_hash(self.archive.read_bytes()) == self.hash

    def _is_installed(self) -> bool:
        LOGGER.debug(f'%s: checking installation', self.__class__.__name__)
        if not self.get_exe().exists():
            LOGGER.debug(f'%s: executable not found', self.__class__.__name__)
            return False
        if not self.get_version() == self.expected_version:
            LOGGER.debug('%s: wrong version: %s (expected %s)',
                         self.__class__.__name__,
                         self.get_version(),
                         self.expected_version
                         )
            return False
        return True

    # pylint: disable=inconsistent-return-statements
    def _download(self) -> bool:
        if self._archive_is_correct():
            LOGGER.debug('%s: archive already downloaded', self.__class__.__name__)
            return True

        LOGGER.debug(f'%s: downloading: %s -> %s', self.__class__.__name__, self.url, self.archive)
        if elib.downloader.download(
                url=self.url,
                outfile=self.archive.absolute(),
                hexdigest=self.hash
        ):
            LOGGER.debug(f'%s: download successful', self.__class__.__name__)
            return True

        LOGGER.error(f'%s: download failed', self.__class__.__name__)
        exit(-1)

    def _extract(self):
        LOGGER.info(f'%s: extracting (this may take a while)', self.__class__.__name__)
        archive = pyunpack.Archive(self.archive)
        patool = _find_patool()
        archive.extractall(directory=self.install_dir, auto_create_dir=True, patool_path=str(patool))
        LOGGER.debug(f'%s: removing archive', self.__class__.__name__)
        # self.archive.unlink()
        LOGGER.info(f'%s: successfully extracted', self.__class__.__name__)

    def setup(self):
        """
        Setup this tool
        """
        if not self._is_installed():
            LOGGER.debug(f'%s: setting up', self.__class__.__name__)
            self._download()
            self._extract()

        LOGGER.debug(f'%s: adding to PATH: %s', self.__class__.__name__, self.get_exe().parent.absolute())
        os.environ['PATH'] = f'{self.get_exe().parent.absolute()};' + os.environ['PATH']
        LOGGER.debug(f'%s: %s', self.__class__.__name__, self.get_version())

    def get_exe(self) -> Path:
        """
        Returns: executable for this tool
        """
        raise NotImplementedError(f'missing exe for {self.__class__.__name__}')

    def get_version(self) -> str:
        """
        Returns: version for this tool
        """
        raise NotImplementedError(f'missing exe for {self.__class__.__name__}')
