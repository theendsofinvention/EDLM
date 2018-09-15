# coding=utf-8
"""
Processes boxes
"""

import re

from edlm.convert._context import Context

_INFO_BOX_RE = re.compile('/info\((?P<text>.*?)\)', flags=re.MULTILINE + re.DOTALL)
_INFO_BOX_REPLACE = r'\\begin{infobox}\n%s\n\end{infobox}'

_ERROR_BOX_RE = re.compile('/error\((?P<text>.*?)\)', flags=re.MULTILINE + re.DOTALL)
_ERROR_BOX_REPLACE = r'\\begin{errorbox}\n%s\n\end{errorbox}'

_BOXES = (
    (_INFO_BOX_RE, _INFO_BOX_REPLACE),
    (_ERROR_BOX_RE, _ERROR_BOX_REPLACE),
)


def process_boxes(ctx: Context):
    for box_re, box_sub in _BOXES:
        while True:
            match = box_re.search(ctx.markdown_text)
            if match:
                print('replacing')
                sub_str = box_sub % match.group('text')
                ctx.markdown_text = box_re.sub(sub_str, ctx.markdown_text, count=1)
            else:
                break
