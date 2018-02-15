# coding=utf-8
from collections import namedtuple

from .markdown import process_markdown
from .tex_template import process_tex_template

TEMPLATE_SETTINGS = namedtuple('TemplateSettings', ['media_dir_main', 'media_dir'])

__all__ = ['process_markdown', 'process_tex_template', 'TEMPLATE_SETTINGS']
