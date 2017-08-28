# coding=utf-8
import logging
import logging.handlers
import os
import re

import click
import click_log
from pkg_resources import DistributionNotFound, get_distribution

from edlm.convert import Convert
from edlm.miktex import MIKTEX

# FIXME: ;C:\Users\bob\AppData\Local\Pandoc\

try:
    __version__ = get_distribution('edlm').version
except DistributionNotFound:
    __version__ = 'not installed'

LOGGER = logging.getLogger('EDLM')
LOGGER.setLevel(logging.DEBUG)


def _check_miktex() -> bool:
    return True
    logging.info('Checking for MikTex installation')
    if not os.path.exists(MIKTEX.pdflatex_path):
        logging.error(f'PDFLatex not found at location: {MIKTEX.pdflatex_path}')
        return False
    else:
        pdflatex_version = MIKTEX.pdflatex_version
        if not pdflatex_version:
            logging.error(f'PDFLatex call failed: {MIKTEX.pdflatex_path}')
            return False

        logging.info(f'PDFLatex version installed: {pdflatex_version}')
        return True


def _setup_miktex() -> bool:
    return True
    if not _check_miktex():
        logging.info('Installing MikTex')
        result = MIKTEX.setup()

        if result:
            logging.info(f'MikTex successfully installed')
            return True

        logging.error(f'Installation of MikTex failed')
        return False

    logging.info(f'MikTex already installed')
    return True


class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    ansi_escape = re.compile(r'\x1b[^m]*m')
    level_remove = re.compile(r'^(debug|warning|info|critical|error): ')

    def emit(self, record: logging.LogRecord):
        record.msg = self.ansi_escape.sub('', record.msg)
        record.msg = self.level_remove.sub('', record.msg)
        super(CustomTimedRotatingFileHandler, self).emit(record)


def _setup_file_logger():
    """
    Setup up logging module to output to the "logs" folder
    """
    try:
        os.makedirs('./logs')
    except FileExistsError:
        pass
    handler = CustomTimedRotatingFileHandler(f'./logs/main.log', when='midnight', backupCount=7)
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(levelname)12s - %(name)30s - %(message)s'
        )
    )
    LOGGER.addHandler(handler)


@click.group()
@click.version_option(version=__version__)
@click_log.simple_verbosity_option(LOGGER, default='INFO')
def cli():
    LOGGER.info(f'EDLM {__version__}')
    _setup_file_logger()


@cli.command()
@click.argument('infile', type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True))
@click.option('-o', '--outfile', help='Output PDF file (defaults to the input file name)')
@click.option('-t', '--title', help='Title of the PDF document (defaults to the input file name)')
def makepdf(infile, outfile, title):
    """
    Converts a Markdown document to PDF
    """
    if not os.path.splitext(infile)[1] == '.md':
        LOGGER.error(f'Invalid value for "infile": Path "{infile}" is not a Markdown file')
    else:
        if not MIKTEX.setup():
            click.secho('MIKTEX setup failed', err=True, fg='red')
        else:
            if _check_miktex():
                click.echo(f'Converting: "{infile}" to PDF')
                convert = Convert()
                convert.make_pdf(infile, outfile, title)


@cli.command()
@click.argument('infile', type=click.Path(exists=True, dir_okay=False, resolve_path=True, readable=True))
@click.option('-o', '--outfile', help='Output Markdown file (defaults to the input file name)')
@click.option('-d', '--outdir', help='Output directory (defaults to the input file name)')
def extractdocx(infile, outfile, outdir):
    """
    Converts a Word (docx) document to markdown.
    """
    if not os.path.splitext(infile) == 'md':
        click.echo(f'Error: Invalid value for "infile": Path "{infile}" is not a docx file')
        convert = Convert()
        convert.make_md(infile, outfile, outdir)


@cli.group()
def convert():
    """
    Converts documents
    """


@convert.command()
@click.argument('in_dir', type=click.Path(exists=True, file_okay=False, resolve_path=True, readable=True))
def pdf(in_dir):
    """
    Converts to PDF
    # """
    # if not MIKTEX.setup():
    #     click.secho('MIKTEX setup failed', err=True, fg='red')
    # else:
    #     if _check_miktex():
    from edlm.convert import convert_source_folder
    convert_source_folder(in_dir)


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
