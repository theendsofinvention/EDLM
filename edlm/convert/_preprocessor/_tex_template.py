# coding=utf-8
"""
Processes Tex templates
"""
from pathlib import Path

import elib
from jinja2 import Environment, FileSystemLoader

from .._context import Context


def _get_jinja_env(template_dir: Path):
    return Environment(
        block_start_string=r'\BLOCK{',
        block_end_string=r'}',
        variable_start_string=r'\VAR{',
        variable_end_string=r'}',
        comment_start_string=r'\#{',
        comment_end_string=r'}',
        line_statement_prefix=r'%%',
        line_comment_prefix=r'%#',
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(str(template_dir.absolute()))
    )


def process_tex_template(ctx: Context) -> str:
    """
    Processes the Tex template

    Adds path the media folders
    """
    ctx.debug(f'processing Tex template file: {ctx.template_file}')

    elib.path.ensure_dir(ctx.template_folder)
    jinja_env = _get_jinja_env(ctx.template_folder)

    media_folders = [folder.absolute() for folder in ctx.media_folders]
    media_folders = [str(folder).replace('\\', '/') for folder in media_folders]
    media_folders = ''.join(f'{{{folder}/}}' for folder in media_folders)
    ctx.debug(f'adding media folders to template: {media_folders}')

    template = jinja_env.get_template(ctx.template_file.name)
    return template.render(**locals())
