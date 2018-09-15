# coding=utf-8
"""
Parses and validate the Markdown front matter
"""
import io
import sys

import yaml

from edlm.convert._context import Context


def _check_front_matter(ctx: Context, front_matter: dict) -> None:
    """
    Verifies all needed keys are present in the front matter

    :param front_matter: front matter to check
    :type front_matter: dict
    """
    missing_keys = set()
    for key in (
        'title', 'qualifier', 'qualifier_short', 'type', 'category', 'title_pictures',
        'header_picture', 'description', 'opr', 'certified_by', 'supersedes',
        'link', 'published_date', 'summary_of_changes'
    ):
        if key not in front_matter:
            missing_keys.add(key)
    if missing_keys:
        ctx.error(f'missing values in "{ctx.index_file}" front matter: {missing_keys}')
        sys.exit(0)




def process_front_matter(ctx: Context) -> None:
    """
    Extracts Markdown front matter from the "index.md" file

    :param ctx: global context
    :type ctx: Context
    """
    _, front_matter_str, _ = ctx.markdown_text.split('---', maxsplit=2)
    front_matter_stream = io.StringIO(front_matter_str)
    # FIXME: catch badly formatted front matter
    front_matter_dict = yaml.safe_load(front_matter_stream)
    _check_front_matter(ctx, front_matter_dict)
    ctx.front_matter = front_matter_dict
    # FIXME: validate front matter dict
