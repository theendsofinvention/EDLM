# coding=utf-8
"""
Final processing of the markdown text
"""

import re

from .._context import Context

RE_DOUBLE_SPACE_AFTER_CMD = re.compile(
    r'\\(?P<cmd>\S+) {2}'
)


def final_processing(ctx: Context):
    """
    Final processing of the markdown text
    """
    ctx.markdown_text = RE_DOUBLE_SPACE_AFTER_CMD.sub(
        r'\g<cmd> ', ctx.markdown_text
    )
