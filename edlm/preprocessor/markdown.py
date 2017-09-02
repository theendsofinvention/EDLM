# coding=utf-8
from edlm import MAIN_LOGGER
from edlm.utils import ensure_file_exists
from .aliases import process_aliases
from .images import process_images

LOGGER = MAIN_LOGGER.getChild(__name__)


def process_markdown(markdown_file: str, settings: dict, media_folders: list) -> str:
    markdown_file = ensure_file_exists(markdown_file)
    LOGGER.debug(f'processing markdown file: {markdown_file}')
    with open(markdown_file) as stream:
        content = stream.read()
    content = process_aliases(content, settings)
    content = process_images(content, settings, media_folders)
    return content
