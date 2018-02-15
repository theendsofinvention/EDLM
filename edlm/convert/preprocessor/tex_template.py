# coding=utf-8
from pathlib import Path

import elib
from jinja2 import Environment, FileSystemLoader

from .._context import Context


def _get_jinja_env(template_dir: Path):
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
        loader=FileSystemLoader(str(template_dir.absolute()))
    )


def process_tex_template(ctx: Context) -> str:
    ctx.debug(f'processing Tex template file: {ctx.template_file}')

    template_dir = elib.path.ensure_dir(ctx.template_folder)
    jinja_env = _get_jinja_env(ctx.template_folder)

    media_folders = ''.join(f'{{{folder}/}}' for folder in ctx.media_folders)
    ctx.debug(f'adding media folders to template: {media_folders}')

    template = jinja_env.get_template(ctx.template_file.name)
    return template.render(**locals())
