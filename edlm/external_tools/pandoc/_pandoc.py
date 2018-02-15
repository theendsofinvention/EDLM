# coding=utf-8

from pathlib import Path

import elib

from edlm import LOGGER as LOGGER, HERE
from edlm.external_tools.base import BaseExternalTool


class Pandoc(BaseExternalTool):

    url = r'https://github.com/pandoc-extras/pandoc-portable/releases/download/2.0.3/pandoc-2.0.3-windows.zip'
    # noinspection SpellCheckingInspection
    hash = '64685f754a28e5d0cfdaf7214e202e53'
    default_archive = Path(HERE, 'pandoc.7z')
    default_install = Path(HERE, 'pandoc')
    expected_version = '2.0.3'

    @property
    def exe(self) -> Path:
        if self._exe is None:
            self._exe = Path(list(Path(self.install_dir).glob('pandoc*'))[-1], 'pandoc.exe').absolute()
        return self._exe

    @property
    def version(self) -> str:
        if self._version is None:
            self._version = elib.run(f'{self.exe} --version', mute=True)[0].split('\n')[0].split(' ')[1]
        return self._version


if __name__ == '__main__':
    m = Pandoc(Path('./pandoc.7z'), Path('./pandoc'))
    m.setup()
    # m._extract()
    # print(m._archive_exists())
    # print(m._archive_is_correct())
    # print(m._download())
    # print(m._archive_exists())
    # print(m._archive_is_correct())
