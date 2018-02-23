# coding=utf-8

from . import Context


def process_hyperlinks(ctx: Context):
    ctx.markdown_text = ctx.markdown_text.replace('\\ref', '\\fullref')
