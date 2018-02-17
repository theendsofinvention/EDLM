# coding=utf-8

import typing
import elib
from pathlib import Path

from . import Context


# def _is_source_folder(source_folder: Path):
#     if not source_folder.is_dir():
#         return False
#     return Path(source_folder, 'index.md').exists()
#
#
# def _get_markdown_files_in_source_folder(source_folder: Path):
#     if _is_source_folder(source_folder):
#         for file in source_folder.iterdir():
#             assert isinstance(file, Path)
#             if file.is_file() and file.name.endswith('.md'):
#                 yield file
#
#
# def _iterate_over_adjacent_source_folders(ctx: Context):
#     for folder in ctx.source_folder.parent.iterdir():
#         yield from _get_markdown_files_in_source_folder(folder)
#
#
# def _gather_markdown_files(ctx: Context):
#     for file in _get_markdown_files_in_source_folder(ctx.source_folder):
#         yield file
#     yield from _iterate_over_adjacent_source_folders(ctx)
#
#
# def _gather_index_md_files(source_folder: Path):
#     pass
#
#
# def _gather_own_includes(ctx: Context, folder: Path):
#     for item in folder.iterdir():
#         assert isinstance(item, Path)
#         if item.is_file() and not item.name == 'index.md' and item.name.endswith('.md'):
#             yield item.absolute().relative_to(ctx.source_folder)
#
#
# def _gather_other_docs(ctx: Context) -> typing.Iterator[Path]:
#     for item in ctx.source_folder.parent.iterdir():
#         if item.is_dir():
#             if item == ctx.source_folder:
#                 continue
#             if Path(item, 'index.md').exists():
#                 yield item.relative_to(ctx.source_folder.parent)
#
#
# def _gather_available_includes_raw(ctx: Context) -> typing.Iterator[Path]:
#     yield from _gather_own_includes(ctx, ctx.source_folder)
#     yield from _gather_other_docs(ctx)
#
#
# def _gather_relative_includes(ctx: Context):
#     for item in _gather_available_includes_raw(ctx):
#         yield item.relative_to(ctx.source_folder.parent)
#
#
# def _process_own_includes(ctx: Context):
#     from . import process_markdown
#     for include in _gather_own_includes(ctx, ctx.source_folder):
#         include_str = f'//include "{include}"'
#         if include_str in ctx.markdown_text:
#             sub_context = ctx.get_sub_context()
#             sub_context.markdown_text = Path(ctx.source_folder, include).read_text()
#             process_markdown(sub_context)
#             ctx.markdown_text.replace(include_str, sub_context.markdown_text)
#             ctx.images_used.update(sub_context.images_used)
#
#
#
# def _process_include_markdown(ctx: Context):
#     pass



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
    include_str = f'//include "{include.relative_to(ctx.source_folder.parent)}"'
    sub_context = ctx.get_sub_context()
    sub_context.source_folder = include
    sub_context.markdown_text = Path(include, 'index.md').read_text()
    sub_context.index_file = include
    sub_context.includes = []
    process_markdown(sub_context)
    ctx.markdown_text = ctx.markdown_text.replace(include_str, sub_context.markdown_text)


def _get_unprocessed_includes(ctx: Context):
    for line_nr, line in enumerate(ctx.markdown_text.split('\n')):
        if '//include' in line:
            ctx.unprocessed_includes.append(f'line {line_nr+1:05d}: {line}')



def process_includes(ctx: Context):
    ctx.unprocessed_includes = []
    for include in ctx.includes:
        if include.is_file():
            _process_local_include(ctx, include)
        elif include.is_dir():
            _process_external_include(ctx, include)

    _get_unprocessed_includes(ctx)
    if ctx.unprocessed_includes:
        ctx.warning(f'there are unprocessed "//include" directives:\n{elib.pretty_format(ctx.unprocessed_includes)}')

