# coding=utf-8
from jinja2 import Environment, FileSystemLoader

from edlm import LOGGER
from edlm.utils import ensure_folder_exists

LOGGER = LOGGER.getChild(__name__)


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


def process_template(template_file_: str,
                     template_folder_: str,
                     media_folders_: list,
                     ) -> str:
    LOGGER.debug(f'processing template file: {template_file_}')

    template_dir = ensure_folder_exists(template_folder_)
    jinja_env = _get_jinja_env(template_folder_)

    media_folders = ''.join(f'{{{folder}/}}' for folder in media_folders_)
    LOGGER.debug(f'adding media folders to template: {media_folders}')

    template = jinja_env.get_template(template_file_)
    return template.render(**locals())
