# coding=utf-8
"""
Processing of Markdown content
"""

from ._aliases import process_aliases
from ._hyperlinks import process_hyperlinks
from ._images import process_images
from ._include import process_includes
from ._references import process_references
from ..._context import Context


def process_markdown(ctx: Context):
    """
    Processing of Markdown content
    """
    ctx.debug(f'processing markdown file: {ctx.index_file}')
    process_aliases(ctx)
    process_images(ctx)
    process_references(ctx)
    process_includes(ctx)
    process_hyperlinks(ctx)
