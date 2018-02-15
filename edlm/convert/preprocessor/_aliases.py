# coding=utf-8
"""
Processes aliases
"""

from .._context import Context


def process_aliases(ctx: Context):
    """
    Processes aliases
    """
    ctx.debug('processing aliases')
    for alias, value in ctx.settings.get('aliases', {}).items():
        ctx.debug(f'processing alias: {alias}')
        ctx.markdown_text = ctx.markdown_text.replace(alias, value)
