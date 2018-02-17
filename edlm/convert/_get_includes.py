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


# def _gather_other_docs(ctx: Context) -> typing.Iterator[Path]:
#     for item in ctx.source_folder.parent.iterdir():
#         if item.is_dir():
#             if item == ctx.source_folder:
#                 continue
#             if Path(item, 'index.md').exists():
#                 yield item.relative_to(ctx.source_folder.parent)


# def _gather_available_includes_raw(ctx: Context) -> typing.Iterator[Path]:
#     yield from _gather_own_includes(ctx, ctx.source_folder)
#     yield from _gather_other_docs(ctx)
#
#
# def _gather_relative_includes(ctx: Context):
#     for item in _gather_available_includes_raw(ctx):
#         yield item.relative_to(ctx.source_folder.parent)

def _gather_indices(folder: Path) -> typing.Iterator[Path]:
    for item in folder.iterdir():
        assert isinstance(item, Path)
        if item.is_file() and not item.name == 'index.md' and item.name.endswith('.md'):
            yield item.absolute()


def _gather_external_includes(ctx: Context) -> typing.Iterator[Path]:
    for item in ctx.source_folder.parent.iterdir():
        assert isinstance(item, Path)
        if item.is_dir() and Path(item, 'index.md').exists():
            yield item.absolute()


def _process_own_includes(ctx: Context):
    for include in _gather_indices(ctx.source_folder):
        relative_include = include.relative_to(ctx.source_folder)
        if f'//include "{relative_include}"' in ctx.markdown_text:
            ctx.includes.append(include)


def _process_external_includes(ctx: Context):
    for include in _gather_external_includes(ctx):
        relative_include = include.relative_to(ctx.source_folder.parent)
        if f'//include "{relative_include}"' in ctx.markdown_text:
            ctx.includes.append(include)


def get_includes(ctx: Context):
    ctx.includes = []
    _process_own_includes(ctx)
    _process_external_includes(ctx)
    ctx.info(f'includes:\n{elib.pretty_format(ctx.includes)}')
    # for x in _gather_available_includes_raw(ctx):
    #     print(x)
    # # exit(0)
    # pass
