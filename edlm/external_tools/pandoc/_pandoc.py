# coding=utf-8
"""
Pandoc external tool
"""

from pathlib import Path

from edlm import HERE
from edlm.external_tools.base import BaseExternalTool


class Pandoc(BaseExternalTool):
    """
    Pandoc external tool
    """

    @property
    def url(self) -> str:
        """Download URL"""
        return r'https://www.dropbox.com/s/f6pccole9mdkuex/pandoc-2.0.3-windows.zip?dl=1'

    @property
    def hash(self) -> str:
        """Expected archive hash"""
        return '64685f754a28e5d0cfdaf7214e202e53'

    @property
    def default_archive(self) -> Path:
        """Expected tool version"""
        return Path(HERE, 'pandoc.7z')

    @property
    def default_install(self) -> Path:
        """Default installation location"""
        return Path(HERE, 'pandoc')

    @property
    def expected_version(self) -> str:
        """Expected tool version"""
        return '2.0.3'

    def get_exe(self) -> Path:  # pragma: no cover
        """
        Returns: Pandoc executable
        """
        return Path(Path(self.install_dir), 'pandoc-2.0.3-windows/pandoc.exe').absolute()

    def get_version(self) -> str:
        """
        Returns: Pandoc version
        """
        version_str = self('--version')
        try:
            return version_str.split('\n')[0].split(' ')[1]
        except IndexError:
            print(version_str)
