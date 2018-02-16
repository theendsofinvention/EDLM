# coding=utf-8
"""
Makes a PDF document from a source folder
"""

import shutil
from pathlib import Path

import elib

from edlm import LOGGER
from edlm.convert._context import Context
from edlm.external_tools import PANDOC

from ._get_index import get_index_file
from ._get_media_folders import get_media_folders
from ._get_settings import get_settings
from ._get_template_folder import get_templates_folder
from ._temp_folder import TempDir
from .preprocessor import process_markdown, process_tex_template

WIDTH_MODIFIER = 0.8
# HEIGHT_MODIFIER = 0.9

PAPER_FORMATS_WIDTH = {
    'a0': 841 * WIDTH_MODIFIER,
    'a1': 594 * WIDTH_MODIFIER,
    'a2': 420 * WIDTH_MODIFIER,
    'a3': 29 * WIDTH_MODIFIER,
    'a4': 210 * WIDTH_MODIFIER,
    'a5': 148 * WIDTH_MODIFIER,
    'a6': 105 * WIDTH_MODIFIER,
    'a7': 74 * WIDTH_MODIFIER,
}


# PAPER_FORMATS_HEIGHT = {
#     'a0': 1189 * HEIGHT_MODIFIER,
#     'a1': 841 * HEIGHT_MODIFIER,
#     'a2': 594 * HEIGHT_MODIFIER,
#     'a3': 420 * HEIGHT_MODIFIER,
#     'a4': 297 * HEIGHT_MODIFIER,
#     'a5': 210 * HEIGHT_MODIFIER,
#     'a6': 148 * HEIGHT_MODIFIER,
#     'a7': 108 * HEIGHT_MODIFIER,
# }


def _set_max_image_width(ctx: Context):
    paper_size = ctx.paper_size.lower()
    if paper_size not in PAPER_FORMATS_WIDTH:
        raise ValueError(paper_size)
    ctx.image_max_width = int(PAPER_FORMATS_WIDTH[paper_size])


# def _get_max_image_height(paper_size: str) -> int:
#     paper_size = paper_size.lower()
#     if paper_size not in PAPER_FORMATS_WIDTH:
#         raise ValueError(paper_size)
#     return int(PAPER_FORMATS_HEIGHT[paper_size])

def _remove_artifacts():
    for item in Path('.').iterdir():
        assert isinstance(item, Path)
        if item.is_dir() and item.name.startswith('__TMP') or item.name.startswith('tex2pdf.'):
            shutil.rmtree(str(item.absolute()))


def _build_folder(ctx: Context):
    ctx.info(f'making PDF')

    # TODO: remove
    ctx.keep_temp_dir = True

    with TempDir(ctx):

        get_media_folders(ctx)

        get_templates_folder(ctx)

        get_index_file(ctx)

        get_settings(ctx)

        ctx.template_file = Path(ctx.temp_dir, 'template.tex').absolute()
        tex_template_text = process_tex_template(ctx)
        ctx.template_file.write_text(tex_template_text, encoding='utf8')

        title = ctx.source_folder.name
        ctx.title = title

        out_folder = elib.path.ensure_dir('.', must_exist=False, create=True)
        ctx.out_folder = out_folder

        for paper_size in ctx.settings['papersize']:
            ctx.paper_size = paper_size
            _set_max_image_width(ctx)

            if paper_size.lower() == 'a4' or len(ctx.settings['papersize']) == 1:
                ctx.out_file = Path(out_folder, f'{title}.PDF').absolute()
            else:
                ctx.out_file = Path(out_folder, f'{title}_{paper_size}.PDF').absolute()

            process_markdown(ctx)

            ctx.source_file = Path(ctx.temp_dir, 'source.md').absolute()
            ctx.source_file.write_text(ctx.markdown_text, encoding='utf8')

            ctx.info(f'building format: {paper_size}')

            ctx.debug(f'context:\n{elib.pretty_format(ctx.__repr__())}')

            pandoc_cmd = [
                '-s',
                '--toc',
                f'--template "{ctx.template_file}"',
                f'--listings "{ctx.source_file}"',
                f'-o "{ctx.out_file}"',
                '-V geometry:margin=1.5cm',
                '-V test',
                '-V geometry:headheight=17pt',
                '-V geometry:includehead',
                '-V geometry:includefoot',
                '-V geometry:heightrounded',
                '-V lot',
                '-V lof',
                f'-V papersize:{ctx.paper_size}',
                '-N',
            ]

            for ref in sorted(ctx.latex_refs):
                pandoc_cmd.append(f'-V refs="{ref}"')

            PANDOC(' '.join(pandoc_cmd))

            # pandoc(
            #     f'-s --toc '
            #     f'--template "{ctx.template_file}" '
            #     f'--listings "{ctx.source_file}" '
            #     # '--filter pandoc-citeproc '
            #     f'-o "{ctx.out_file}" '
            #     f'-V geometry:margin=1.5cm '
            #     f'-V refs={ctx.references} '
            #     f'-V test '
            #     f'-V geometry:headheight=17pt '
            #     f'-V geometry:includehead '
            #     f'-V geometry:includefoot '
            #     f'-V geometry:heightrounded '
            #     f'-V lot '
            #     f'-V lof '
            #     f'-V papersize:{ctx.paper_size} '
            #     f'-N',
            # )


def _is_source_folder(folder: Path) -> bool:
    if not folder.is_dir():
        return False
    return Path(folder, 'index.md').exists()


def make_pdf(ctx: Context, source_folder: Path):
    """
    Makes a PDF document from a source folder

    Args:
        ctx: Context
        source_folder: source folder
    """
    _remove_artifacts()

    source_folder = elib.path.ensure_dir(source_folder).absolute()

    LOGGER.info(f'analyzing folder: "{source_folder}"')

    if _is_source_folder(source_folder):
        ctx.source_folder = source_folder
        _build_folder(ctx)

    else:
        for child in source_folder.iterdir():
            if _is_source_folder(child):
                ctx.source_folder = child.absolute()
                _build_folder(ctx)
