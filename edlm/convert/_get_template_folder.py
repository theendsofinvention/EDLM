# coding=utf-8

from pathlib import Path

from ._context import Context


def get_template_folder(ctx: Context):
    ctx.debug('looking for templates folder')
    search_path = Path(ctx.source_folder).absolute()
    while not ctx.template_folder:
        ctx.debug(f'looking for templates folder in: {search_path}')
        template_folder = search_path.joinpath('templates').absolute()
        if template_folder.exists() and template_folder.is_dir():
            ctx.info(f'template folder found: {template_folder}')
            ctx.template_folder = template_folder
        if len(search_path.parents) == 1:
            raise FileNotFoundError('unable to find a "templates" d irectory')
        search_path = search_path.parent.absolute()
