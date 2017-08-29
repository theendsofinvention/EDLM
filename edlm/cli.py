# coding=utf-8
import logging
import logging.handlers
import os
import re

import click
from pkg_resources import DistributionNotFound, get_distribution

from edlm.convert import Convert
from edlm.config import CFG
from edlm.utils.click_logger import install_click_logger

try:
    __version__ = get_distribution('edlm').version
except DistributionNotFound:
    __version__ = 'not installed'

LOGGER = logging.getLogger('EDLM')
LOGGER.setLevel(logging.DEBUG)


class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    ansi_escape = re.compile(r'\x1b[^m]*m')
    level_remove = re.compile(r'^(debug|warning|info|critical|error): ')

    def emit(self, record: logging.LogRecord):
        record.msg = self.ansi_escape.sub('', record.msg)
        record.msg = self.level_remove.sub('', record.msg)
        super(CustomTimedRotatingFileHandler, self).emit(record)


def _setup_logging(level=logging.INFO):
    """
    Setup up logging module to output to the "logs" folder
    """
    try:
        os.makedirs('./logs')
    except FileExistsError:
        pass
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)12s - %(name)s.%(funcName)s[%(lineno)s] - %(message)s'
    )
    handler = CustomTimedRotatingFileHandler(f'./logs/main.log', when='midnight', backupCount=7)
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    install_click_logger(LOGGER, formatter, level)


@click.group()
@click.version_option(version=__version__)
@click.option('-v', '--verbose', default=False, help='Outputs DEBUG message on console')
def cli(verbose):
    LOGGER.info(f'EDLM {__version__}')
    print(CFG.debug)
    if verbose:
        _setup_logging(logging.DEBUG)
    else:
        _setup_logging()


@cli.command()
@click.argument('infile', type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True))
@click.option('-o', '--outfile', help='Output Markdown file (defaults to the input file name)')
@click.option('-d', '--outdir', help='Output directory (defaults to the input file name)')
def extractdocx(infile, outfile, outdir):
    """
    Converts a Word (docx) document to markdown.
    """
    if not os.path.splitext(infile) == 'md':
        LOGGER.error(f'Invalid value for "infile": Path "{infile}" is not a docx file')
        return

    converter = Convert()
    converter.make_md(infile, outfile, outdir)


@cli.group()
def convert():
    """
    Converts documents
    """


@convert.command()
@click.argument(
    'source_folder',
    type=click.Path(exists=True, file_okay=False, resolve_path=True, readable=True),
)
@click.option('-k', '--keep-temp-dir', default=False, help='Keep temporary folder')
def pdf(source_folder, keep_temp_dir):
    """
    Converts content of SOURCE_FOLDER to PDF
    """
    from edlm.convert import convert_source_folder
    convert_source_folder(source_folder, keep_temp_dir)


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
