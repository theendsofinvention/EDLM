# coding=utf-8
import inspect
import typing
from pathlib import Path

import elib

from edlm import LOGGER


class Context:
    source_folder: Path = None
    keep_temp_dir: bool = False
    paper_size: str = None
    temp_dir: Path = None
    media_folders: typing.List[str] = None
    template_folder: Path = None
    index_file: Path = None
    settings: dict = None
    template_file: Path = None
    title: str = None
    out_folder: Path = None
    out_file: Path = None
    source_file: Path = None
    markdown_text: str = None

    caption: str = None
    image: str = None
    extras: str = None
    max_image_width: int = None
    width: int = None
    width_str: str = None

    def debug(self, text):
        LOGGER.debug(f'"{self.source_folder}": {text}')

    def info(self, text):
        LOGGER.info(f'"{self.source_folder}": {text}')

    def error(self, text):
        LOGGER.error(f'"{self.source_folder}": {text}')

    def warning(self, text):
        LOGGER.warning(f'"{self.source_folder}": {text}')

    def __repr__(self):
        out = {}
        for name, value in inspect.getmembers(self):
            if name.startswith('_'):
                continue
            if callable(getattr(self, name)):
                continue
            if name in ['markdown_text']:
                continue
            out[name] = value

        return elib.pretty_format(out)
