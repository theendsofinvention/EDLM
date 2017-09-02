# coding=utf-8
from collections import namedtuple

from edlm import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)

TEMPLATE_SETTINGS = namedtuple('TemplateSettings', ['media_dir_main', 'media_dir'])

from .markdown import process_markdown
from .template import process_template

__all__ = ['process_markdown', 'process_template', 'TEMPLATE_SETTINGS']
