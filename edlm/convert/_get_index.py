# coding=utf-8


from pathlib import Path

import elib

from ._context import Context


def get_index_file(ctx: Context) -> Path:
    index_file = elib.path.ensure_file(ctx.source_folder, 'index.md')
    ctx.debug(f'index file: {index_file}')
    ctx.index_file = index_file
    return index_file
