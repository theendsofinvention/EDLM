# coding=utf-8

import typing
from pathlib import Path

from edlm import LOGGER, HERE
from edlm.external_tools.base import BaseExternalTool

STR_OR_PATH = typing.Union[str, Path]


class MikTex(BaseExternalTool):

    url = r'https://miktex.org/download/ctan/systems/win32/miktex/setup/miktex-portable-2.9.6521.exe'
    hash = 'c8164da05a93b7f00eb79cba7d9ce611'
    default_archive = Path(HERE, 'miktex.7z').absolute()
    default_install = Path(HERE, 'miktex').absolute()
    expected_version = '2.9.6354'

    @property
    def version(self) -> str:
        if self._version is None:
            self._version = self('--version', mute=True).split('\n')[0].split(' ')[1]
        return self._version

    @property
    def exe(self) -> Path:
        if self._exe is None:
            self._exe = Path(self.install_dir, 'texmfs/install/miktex/bin/pdflatex.exe').absolute()
        return self._exe


if __name__ == '__main__':
    m = MikTex(Path('./miktex.7z'), Path('./miktex'))
    m.setup()
    # print(m._archive_exists())
    # print(m._archive_is_correct())
    # m._download()
    # print(m._archive_exists())
    # print(m._archive_is_correct())
