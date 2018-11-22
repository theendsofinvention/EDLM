# coding=utf-8
"""
Converts \ref into \\fullref
"""

from edlm.convert._context import Context


def process_hyperlinks(ctx: Context):
    """
    Converts \ref into \\fullref
    """
    ctx.markdown_text = ctx.markdown_text.replace('\\ref', '\\fullref')
