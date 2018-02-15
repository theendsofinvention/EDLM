# coding=utf-8

import re

from .._context import Context

RE_DOUBLE_SPACE_AFTER_CMD = re.compile(
    r'\\(?P<cmd>\S+) {2}'
)


def final_processing(ctx: Context):
    ctx.markdown_text = RE_DOUBLE_SPACE_AFTER_CMD.sub(
        '\g<cmd> ', ctx.markdown_text
    )
