# coding=utf-8
import os
from edlm import MAIN_LOGGER
from edlm.utils import ensure_file_exists, ensure_folder_exists
from collections import namedtuple
from jinja2 import Environment, Template, FileSystemLoader


LOGGER = MAIN_LOGGER.getChild(__name__)


def _process_aliases(content: str, settings: dict) -> str:
    LOGGER.debug('processing aliases')
    for alias, value in settings.get('aliases', {}).items():
        LOGGER.debug(f'processing alias: {alias}')
        content = content.replace(alias, value)
    return content


def process_markdown(markdown_file: str, settings: dict) -> str:
    markdown_file = ensure_file_exists(markdown_file)
    LOGGER.debug(f'processing markdown file: {markdown_file}')
    with open(markdown_file) as stream:
        content = stream.read()
    content = _process_aliases(content, settings)
    return content


TEMPLATE_SETTINGS = namedtuple('TemplateSettings', ['media_dir_main', 'media_dir'])

def _get_jinja_env(template_dir: str):
    return Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(template_dir)
    )


def process_template(template_file: str,
                     template_folder: str,
                     media_folder_main,
                     media_folder,
                     ) -> str:
    LOGGER.debug(f'processing template file: {template_file}')
    template_dir = ensure_folder_exists(template_folder)
    jinja_env = _get_jinja_env(template_folder)

    template = jinja_env.get_template(template_file)
    return template.render(**locals())

