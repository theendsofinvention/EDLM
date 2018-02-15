# coding=utf-8
"""
Pandoc external tool
"""

from pathlib import Path

import elib

from edlm import HERE
from edlm.external_tools.base import BaseExternalTool


class Pandoc(BaseExternalTool):
    """
    Pandoc external tool
    """
    url = r'https://www.dropbox.com/s/f6pccole9mdkuex/pandoc-2.0.3-windows.zip?dl=1'
    # noinspection SpellCheckingInspection
    hash = '64685f754a28e5d0cfdaf7214e202e53'
    default_archive = Path(HERE, 'pandoc.7z')
    default_install = Path(HERE, 'pandoc')
    expected_version = '2.0.3'

    @property
    def exe(self) -> Path:
        """

        Returns: Pandoc executable

        """
        if self._exe is None:
            self._exe = Path(list(Path(self.install_dir).glob('pandoc*'))[-1], 'pandoc.exe').absolute()
        return self._exe

    @property
    def version(self) -> str:
        """

        Returns: Pandoc version

        """
        if self._version is None:
            self._version = elib.run(f'{self.exe} --version', mute=True)[0].split('\n')[0].split(' ')[1]
        return self._version
