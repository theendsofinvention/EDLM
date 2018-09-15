# coding=utf-8
"""
Parses and validate the Markdown front matter
"""

import io

import yaml

from edlm.convert._context import Context


def process_front_matter(ctx: Context) -> None:
    """
    Extracts Markdown front matter from the "index.md" file

    :param ctx: global context
    :type ctx: Context
    """
    _, front_matter_str, _ = ctx.markdown_text.split('---', maxsplit=2)
    front_matter_stream = io.StringIO(front_matter_str)
    # FIXME: catch badly formatted front matter
    ctx.front_matter = yaml.safe_load(front_matter_stream)
    # FIXME: validate front matter dict
