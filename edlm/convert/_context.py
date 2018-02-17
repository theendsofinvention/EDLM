# coding=utf-8
"""
Global context
"""
import typing
from pathlib import Path

import elib

from edlm import LOGGER
from ._settings import Settings

DEFAULT = {
    'source_folder': None,
    'paper_size': 'a4',
    'title': None,
    'markdown_text': None,

    'temp_dir': None,
    'keep_temp_dir': False,
    'media_folders': None,
    'index_file': None,
    'out_folder': None,
    'out_file': None,
    'source_file': None,

    'settings': None,
    'settings_files': None,

    'template_source': None,
    'template_file': None,

    'image_caption': None,
    'image_current': None,
    'image_extras': None,
    'image_max_width': None,
    'image_width': None,
    'image_width_str': None,
    'images_used': None,

    'latex_refs': None,
}


class _Val:
    def __init__(self, instance):
        self.instance = instance

    def _return_default(self):
        try:
            return DEFAULT[self.name]
        except KeyError:
            raise KeyError(f'CONTEXT: no default value for {self.name}')

    def __get__(self, instance, owner):
        try:
            return instance.data[self.name]
        except KeyError:
            return self._return_default()

    def __set__(self, instance, value):
        if value is not None and not isinstance(value, self.instance):
            raise TypeError(f'CONTEXT: expected "{self.instance}" for "{self.name}", got "{type(value)}"')
        instance.data[self.name] = value

    # this is the new initializer:
    def __set_name__(self, owner, name):
        self.name = name  # pylint: disable=attribute-defined-outside-init


class Context:
    """
    Global context
    """
    source_folder: Path = _Val(Path)
    paper_size: str = _Val(str)
    title: str = _Val(str)
    markdown_text: str = _Val(str)

    temp_dir: Path = _Val(Path)
    keep_temp_dir: bool = _Val(bool)
    media_folders: list = _Val(list)
    index_file: Path = _Val(Path)
    out_folder: Path = _Val(Path)
    out_file: Path = _Val(Path)
    source_file: Path = _Val(Path)

    settings: Settings = _Val(Settings)
    settings_files: list = _Val(list)

    template_source: Path = _Val(Path)
    template_file: Path = _Val(Path)

    image_caption: str = _Val(str)
    image_current: str = _Val(str)
    image_extras: str = _Val(str)
    image_max_width: int = _Val(int)
    image_width: int = _Val(int)
    image_width_str: str = _Val(str)
    images_used: set = _Val(set)

    latex_refs: _Val(list)

    def __init__(self):
        self.data = {}
        self.skip_repr = ['markdown_text']
        self.settings = Settings()

    def debug(self, text):
        """
        Convenient shortcut to main EDLM LOGGER
        """
        LOGGER.debug(f'"{self.source_folder}": {text}')

    def info(self, text):
        """
        Convenient shortcut to main EDLM LOGGER
        """
        LOGGER.info(f'"{self.source_folder}": {text}')

    def error(self, text):
        """
        Convenient shortcut to main EDLM LOGGER
        """
        LOGGER.error(f'"{self.source_folder}": {text}')

    def warning(self, text):
        """
        Convenient shortcut to main EDLM LOGGER
        """
        LOGGER.warning(f'"{self.source_folder}": {text}')

    def __repr__(self):  # pylint: disable=bad-continuation
        return elib.pretty_format({k: v for k, v in self.data.items() if k not in self.skip_repr})

