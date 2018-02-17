# coding=utf-8
"""
Replaces include directive with the actual markdown content
"""

from pathlib import Path

import elib

from . import Context


def _process_local_include(ctx: Context, include: Path):
    from . import process_markdown
    include_str = f'//include "{include.relative_to(ctx.source_folder)}"'
    sub_context = ctx.get_sub_context()
    sub_context.markdown_text = Path(ctx.source_folder, include).read_text()
    sub_context.index_file = include
    sub_context.includes = []
    process_markdown(sub_context)
    ctx.markdown_text = ctx.markdown_text.replace(include_str, sub_context.markdown_text)
    ctx.images_used.update(sub_context.images_used)


def _process_external_include(ctx: Context, include: Path):
    from . import process_markdown
    from ..._get_includes import get_includes
    include_str = f'//include "{include.relative_to(ctx.source_folder.parent)}"'
    sub_context = ctx.get_sub_context()
    sub_context.source_folder = include
    sub_context.markdown_text = Path(include, 'index.md').read_text()
    sub_context.index_file = include
    sub_context.includes = []
    get_includes(sub_context)
    process_markdown(sub_context)
    ctx.markdown_text = ctx.markdown_text.replace(include_str, sub_context.markdown_text)


def _get_unprocessed_includes(ctx: Context):
    for line_nr, line in enumerate(ctx.markdown_text.split('\n')):
        if '//include' in line:
            ctx.unprocessed_includes.append(f'line {line_nr+1:05d}: {line}')


def process_includes(ctx: Context):
    """
    Replaces include directive with the actual markdown content

    Args:
        ctx: Context
    """
    ctx.unprocessed_includes = []
    for include in ctx.includes:
        if include.is_file():
            _process_local_include(ctx, include)
        elif include.is_dir():
            _process_external_include(ctx, include)

    _get_unprocessed_includes(ctx)
    if ctx.unprocessed_includes:
        ctx.warning(f'there are unprocessed "//include" directives:\n{elib.pretty_format(ctx.unprocessed_includes)}')
