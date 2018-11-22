# coding=utf-8
"""
Command line interface
"""
import logging
import sys

import click

from edlm import __version__
from edlm.config import CFG
from edlm.convert import Context, make_pdf
from edlm.external_tools import MIKTEX, PANDOC


def _setup_logging():
    format_str = '%(relativeCreated)10d ms ' \
                 '%(levelname)8s ' \
                 '[%(pathname)s@%(lineno)d %(funcName)s]: ' \
                 '%(message)s'
    formatter = logging.Formatter(format_str)
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(formatter)
    _console_handler.setLevel(logging.DEBUG)
    _file_handler = logging.FileHandler('edlm.log', mode='w', encoding='utf8')
    _file_handler.setFormatter(formatter)
    _file_handler.setLevel(logging.DEBUG)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(_file_handler)
    LOGGER.addHandler(_console_handler)
    elib_run_logger = logging.getLogger('elib_run')
    elib_run_logger.setLevel(logging.INFO)
    elib_run_logger.addHandler(_console_handler)


LOGGER = logging.getLogger('EDLM')


@click.group()
@click.version_option(version=__version__)
@click.option('--debug', '-d', default=False, help='Outputs DEBUG message on console', is_flag=True)
def cli(debug):
    """
    Command line interface
    """
    _setup_logging()
    debug = debug or CFG.debug
    handlers = (handler for handler in LOGGER.handlers if not isinstance(handler, logging.FileHandler))
    if not debug:
        for handler in handlers:
            handler.setLevel(logging.INFO)

    LOGGER.info(__version__)

    PANDOC.setup()
    MIKTEX.setup()


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
@click.option('-k', '--keep-temp-dir', default=False, help='Keep temporary folder', is_flag=True)
@click.option('-f', '--force', default=False, help='Force re-generation of documents', is_flag=True)
def pdf(source_folder, keep_temp_dir, force):
    """
    Converts content of SOURCE_FOLDER(s) recursively for folders containing "index.md" files and convert them to PDF
    """

    ctx = Context()
    ctx.keep_temp_dir = keep_temp_dir or CFG.keep_temp_dir
    ctx.regen = force

    for folder in source_folder:
        make_pdf(ctx, folder)


# noinspection SpellCheckingInspection
if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    exit(0)
