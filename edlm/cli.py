# coding=utf-8
"""
Command line interface
"""

import click
import elib

from edlm import LOGGER, __version__
from edlm.config import CFG
from edlm.convert import Context, make_pdf
from edlm.external_tools import MIKTEX, PANDOC


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

    ctx = Context()
    ctx.keep_temp_dir = keep_temp_dir

    for folder in source_folder:
        make_pdf(ctx, folder)


# noinspection SpellCheckingInspection
if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    exit(0)
