# coding=utf-8
"""
Processing of Markdown content
"""

from ..._context import Context
from ._aliases import process_aliases
from ._final_processing import final_processing
from ._images import process_images
from ._references import process_references
from ._symbols import process_symbols


def process_markdown(ctx: Context):
    """
    Processing of Markdown content
    """
    ctx.debug(f'processing markdown file: {ctx.index_file}')
    ctx.markdown_text = ctx.index_file.read_text(encoding='utf8')
    process_aliases(ctx)
    process_images(ctx)
    process_symbols(ctx)
    process_references(ctx)
    final_processing(ctx)
