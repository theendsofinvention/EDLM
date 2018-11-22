# coding=utf-8
"""
Base class for external tools
"""
import abc
import functools
import logging
import os
import sys
import typing
from pathlib import Path

import elib
import elib_run

from edlm import HERE

LOGGER = logging.getLogger('EDLM')

StrOrPath = typing.Union[str, Path]


@functools.lru_cache(1)
def _find_7za() -> Path:
    LOGGER.debug('looking for 7za.exe')
    _7za_path = Path(HERE, 'edlm/vendor/7za.exe').absolute()
    if not _7za_path.exists():
        LOGGER.error('unable to find 7za.exe: %s', str(_7za_path))
        sys.exit(1)
    return _7za_path


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

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """Download URL"""

    @property
    @abc.abstractmethod
    def hash(self) -> str:
        """Expected archive hash"""

    @property
    @abc.abstractmethod
    def default_install(self) -> Path:
        """Default installation location"""

    @property
    @abc.abstractmethod
    def default_archive(self) -> Path:
        """Default archive name"""

    @property
    @abc.abstractmethod
    def expected_version(self) -> str:
        """Expected tool version"""

    def __init__(self, archive: StrOrPath = None, install_dir: StrOrPath = None) -> None:
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
        out, code = elib_run.run(str(self.get_exe().absolute()) + ' ' + cmd, timeout=120)
        if code != 0:
            LOGGER.error(out)
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
        _7za_path = _find_7za()
        LOGGER.info(f'%s: extracting (this may take a while)', self.__class__.__name__)
        LOGGER.debug(f'%s: extracting to: %s', self.__class__.__name__, self.install_dir)
        print(self.archive)
        archive_str = str(self.archive.absolute()).replace('\\', '/')
        elib_run.run(fr'{str(_7za_path)} x {archive_str} -otools -y')
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
