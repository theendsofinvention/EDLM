# coding=utf-8
from edlm import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)


def process_aliases(content: str, settings: dict) -> str:
    LOGGER.debug('processing aliases')
    for alias, value in settings.get('aliases', {}).items():
        LOGGER.debug(f'processing alias: {alias}')
        content = content.replace(alias, value)
    return content