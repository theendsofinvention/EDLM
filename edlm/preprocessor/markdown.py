# coding=utf-8

import elib

from edlm import LOGGER

from .aliases import process_aliases
from .images import process_images

LOGGER = LOGGER.getChild(__name__)


def process_markdown(markdown_file: str, settings: dict, media_folders: list) -> str:
    markdown_file = elib.path.ensure_file(markdown_file)

    LOGGER.debug(f'processing markdown file: {markdown_file}')
    with open(markdown_file) as stream:
        content = stream.read()

    content = process_aliases(content, settings)
    content = process_images(content, settings, media_folders)

    return content
