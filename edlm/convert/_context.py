# coding=utf-8
"""
Global context
"""
import inspect
import typing
from pathlib import Path

import elib

from edlm import LOGGER


class Context:
    """
    Global context
    """
    source_folder: Path = None
    keep_temp_dir: bool = False
    paper_size: str = None
    temp_dir: Path = None
    media_folders: typing.List[Path] = None
    index_file: Path = None
    title: str = None
    out_folder: Path = None
    out_file: Path = None
    source_file: Path = None
    markdown_text: str = None

    settings: dict = None
    settings_files: list = None

    template_source: Path = None
    template_file: Path = None

    image_caption: str = None
    image_current: str = None
    image_extras: str = None
    image_max_width: int = None
    image_width: int = None
    image_width_str: str = None
    images_used: set = None

    used_references: set = None
    latex_refs: list = None

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
