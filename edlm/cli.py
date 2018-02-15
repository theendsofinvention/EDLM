# coding=utf-8
"""
Command line interface
"""

import click
import elib

from edlm import LOGGER, __version__
from edlm.config import CFG
from edlm.convert import Context
from edlm.external_tools import MIKTEX, PANDOC

LOGGER = LOGGER.getChild(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option('--debug', default=False, help='Outputs DEBUG message on console', is_flag=True)
def cli(debug):
    """
    Command line interface
    """
    LOGGER.info(f'EDLM {__version__}')
    debug = debug or CFG.debug
    if debug:
        elib.custom_logging.set_handler_level('EDLM', 'ch', 'debug')
    else:
        elib.custom_logging.set_handler_level('EDLM', 'ch', 'info')
    PANDOC.setup()
    MIKTEX.setup()


# @cli.command()
# @click.argument('infile', type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True))
# @click.option('-o', '--outfile', help='Output Markdown file (defaults to the input file name)')
# @click.option('-d', '--outdir', help='Output directory (defaults to the input file name)')
# def extractdocx(infile, outfile, outdir):
#     """
#     Converts a Word (docx) document to markdown.
#     """
#     if not os.path.splitext(infile) == 'md':
#         LOGGER.error(f'Invalid value for "infile": Path "{infile}" is not a docx file')
#         return
#
#     converter = Convert()
#     converter.make_md(infile, outfile, outdir)


@cli.group()
def convert():
    """
    Converts documents
    """


@convert.command()
@click.argument(
    'source_folder',
    type=click.Path(exists=True, file_okay=False, resolve_path=True, readable=True),
    nargs=-1,
)
@click.option('--keep-temp-dir', default=False, help='Keep temporary folder', is_flag=True)
def pdf(source_folder, keep_temp_dir):
    """
    Converts content of SOURCE_FOLDER(s) recursively for folders containing "index.md" files and convert them to PDF
    """

    from edlm.convert import make_pdf

    ctx = Context()
    ctx.keep_temp_dir = keep_temp_dir

    for folder in source_folder:
        make_pdf(ctx, folder)


# noinspection SpellCheckingInspection
if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    exit(0)

    # os.environ['PATH'] += os.pathsep + r'F:\DEV\test-doc\miktex\texmfs\install\miktex\bin'

    # for f in glob.glob('./*.docx'):
    #     print(f)
    #
    #     subprocess.check_call(
    #         [
    #             'pandoc',
    #             '-s',
    #             '--extract-media=.',
    #             # '-S',
    #             # '-t', 'rst',
    #             f,
    #             '-o',
    #             './test3.md',
    #             # '-V', 'geometry:margin=1in',
    #         ]
    #     )

    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         '-s',
    #         '-t', 'markdown-simple_tables-grid_tables-pipe_tables',
    #         # '--extract-media=.',
    #         # '-S',
    #         # '-t', 'rst',
    #         './132 617th SOP 2.1.docx',
    #         '-o',
    #         './multiline.md',
    #     ]
    # )
    #
    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         '-s',
    #         '-t', 'markdown-simple_tables-grid_tables-multiline_tables',
    #         # '--extract-media=.',
    #         # '-S',
    #         # '-t', 'rst',
    #         './132 617th SOP 2.1.docx',
    #         '-o',
    #         './pipe.md',
    #     ]
    # )
    #
    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         '-s',
    #         '-t', 'markdown-simple_tables-pipe_tables-multiline_tables',
    #         # '--extract-media=.',
    #         # '-S',
    #         # '-t', 'rst',
    #         './132 617th SOP 2.1.docx',
    #         '-o',
    #         './grid.md',
    #     ]
    # )
    #
    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         '-s',
    #         '-t', 'markdown-pipe_tables-grid_tables-multiline_tables',
    #         # '--extract-media=.',
    #         # '-S',
    #         # '-t', 'rst',
    #         './132 617th SOP 2.1.docx',
    #         '-o',
    #         './simple.md',
    #     ]
    # )

    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         '-s',
    #         '--toc',
    #         '--template', './templates/template.tex',
    #         # '-B', './templates/617th_title_page.tex',
    #         'test.md',
    #         '-o',
    #         './test.pdf',
    #         '-V', 'geometry:margin=2.5cm',
    #         '-V', 'lot',
    #         '-V', 'lof',
    #         '-V', 'title=SOP'
    #     ]
    # )

    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         '-s',
    #         'test.tex',
    #         '-o',
    #         './test.pdf',
    #     ]
    # )

    # subprocess.check_call(
    #     [
    #         'pandoc',
    #         './test.md',
    #         '-o',
    #         './test.pdf'
    #     ]
    # )
