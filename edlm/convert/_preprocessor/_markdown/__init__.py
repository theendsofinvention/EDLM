# coding=utf-8
"""
Processing of Markdown content
"""

from edlm.convert._context import Context
from edlm.convert._preprocessor._markdown._aliases import process_aliases
from edlm.convert._preprocessor._markdown._boxes import process_boxes
from edlm.convert._preprocessor._markdown._front_matter import process_front_matter
from edlm.convert._preprocessor._markdown._hyperlinks import process_hyperlinks
from edlm.convert._preprocessor._markdown._images import process_images
from edlm.convert._preprocessor._markdown._include import process_includes
from edlm.convert._preprocessor._markdown._references import process_references


def process_markdown(ctx: Context, skip_front_matter: bool = False):
    """
    Processing of Markdown content
    """
    ctx.debug(f'processing markdown file: {ctx.index_file}')
    process_aliases(ctx)
    process_images(ctx)
    process_references(ctx)
    process_includes(ctx)
    process_hyperlinks(ctx)
    process_boxes(ctx)
    if not skip_front_matter and ctx.index_file.name == 'index.md':
        process_front_matter(ctx)
