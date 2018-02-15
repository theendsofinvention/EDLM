# coding=utf-8
"""
Base class for external tools
"""
import os
import sys
import typing
from pathlib import Path

import elib
import pyunpack

from edlm import LOGGER
from edlm.utils import download, get_hash

LOGGER = LOGGER

STR_OR_PATH = typing.Union[str, Path]


def _find_patool() -> Path:
    python_exe = Path(sys.executable).absolute()
    LOGGER.debug(f'python_exe: {python_exe}')
    patool_path = Path(python_exe.parent, 'patool')
    if patool_path.exists():
        return patool_path.absolute()

    scripts_path = Path(python_exe, 'scripts')
    if scripts_path.exists() and scripts_path.is_dir():
        patool_path = Path(scripts_path, 'patool')
        if patool_path.exists():
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

    def __init__(self, archive: STR_OR_PATH = None, install_dir: STR_OR_PATH = None):
        self.__check_values()

        if archive is None:
            archive = self.default_archive
        if install_dir is None:
            install_dir = self.default_install

        self.archive = elib.path.ensure_file(archive, must_exist=False).absolute()
        self.install_dir = elib.path.ensure_dir(install_dir, must_exist=False).absolute()

        LOGGER.debug(f'{self.__class__.__name__}: archive: {self.archive}')
        LOGGER.debug(f'{self.__class__.__name__}: install dir: {self.install_dir}')

        self._exe = None
        self._version = None

    def __call__(
            self,
            cmd: str,
            cwd: str = '.',
            mute: bool = True,
            filters: typing.Union[None, typing.Iterable[str]] = None,
            failure_ok: bool = False,
    ):
        out, _ = elib.run(
            str(self.exe.absolute()) + ' ' + cmd,
            cwd=cwd, mute=mute, filters=filters, failure_ok=failure_ok
        )
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

    def _archive_exists(self) -> bool:
        return self.archive.exists()

    def _archive_is_correct(self) -> bool:
        try:
            if not self._archive_exists():
                return False
            return get_hash(self.archive.read_bytes()) == self.hash
        except IndexError:
            return False

    def _is_installed(self) -> bool:
        LOGGER.debug(f'{self.__class__.__name__}: checking installation')
        try:
            if not self.exe.exists():
                LOGGER.debug(f'{self.__class__.__name__}: executable not found')
                return False
        except IndexError:
            return False
        if not self.version == self.expected_version:
            LOGGER.debug(f'{self.__class__.__name__}: wrong version: '
                         f'{self.version} '
                         f'(expected {self.expected_version})')
            return False
        return True

    # pylint: disable=inconsistent-return-statements
    def _download(self) -> bool:
        if self._archive_is_correct():
            LOGGER.debug('{self.__class__.__name__}: archive already downloaded')
            return True

        LOGGER.debug(f'{self.__class__.__name__}: downloading: {self.url} -> {self.archive}')
        if download(
                url=self.url,
                outfile=self.archive.absolute(),
                hexdigest=self.hash
        ):
            LOGGER.debug(f'{self.__class__.__name__}: download successful')
            return True
        else:
            LOGGER.error(f'{self.__class__.__name__}: download failed')
            exit(-1)

    def _extract(self):
        LOGGER.info(f'{self.__class__.__name__}: extracting (this may take a while)')
        archive = pyunpack.Archive(self.archive)
        patool = _find_patool()
        archive.extractall(directory=self.install_dir, auto_create_dir=True, patool_path=str(patool))
        LOGGER.info(f'{self.__class__.__name__}: successfully extracted')

    def setup(self):
        """
        Setup this tool
        """
        if not self._is_installed():
            LOGGER.debug(f'{self.__class__.__name__}: setting up')
            self._download()
            self._extract()

        LOGGER.debug(f'{self.__class__.__name__}: adding to PATH: {self.exe.parent.absolute()}')
        os.environ['PATH'] = f'{self.exe.parent.absolute()};' + os.environ['PATH']
        LOGGER.debug(f'{self.__class__.__name__}: {self.version}')

    @property
    def exe(self) -> Path:
        """

        Returns: executable for this tool

        """
        raise NotImplementedError(f'missing exe for {self.__class__.__name__}')

    @property
    def version(self) -> str:
        """

        Returns: version

        """
        raise NotImplementedError(f'missing version for {self.__class__.__name__}')
