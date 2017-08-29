# coding=utf-8
import glob
import os
import yaml
import pprint
import shutil
import tempfile
import re

from edlm import MAIN_LOGGER
from edlm.preprocessor import process_markdown, process_template
from edlm.settings import read_settings, update_settings
from edlm.utils import do, ensure_file_exists, ensure_folder_exists

LOGGER = MAIN_LOGGER.getChild(__name__)

import collections


def update_nested_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update_nested_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def _get_temp_folder():
    temp_dir = ensure_folder_exists(tempfile.mkdtemp(dir='.'))
    LOGGER.debug(f'using temporary folder: {temp_dir}')
    return temp_dir


def _get_template_folder(source_folder: str) -> str:
    template_folder = os.path.join(
        os.path.dirname(source_folder),
        './templates'
    )
    template_folder = ensure_folder_exists(template_folder)
    LOGGER.debug(f'template_folder: {template_folder}')
    return template_folder


def _get_index_file(source_folder: str) -> str:
    index_file = ensure_file_exists(os.path.join(source_folder, 'index.md'))
    LOGGER.debug(f'index file: {index_file}')
    return index_file


def _get_settings(source_folder: str) -> dict:
    LOGGER.info('reading settings')

    settings = {}
    settings_files = []

    while True:
        LOGGER.debug(f'traversing: {source_folder}')
        file = os.path.join(source_folder, 'settings.yml')
        if os.path.exists(file) and os.path.isfile(file):
            LOGGER.info(f'settings file found: {file}')
            settings_files.append(file)
        if os.path.ismount(source_folder):
            LOGGER.debug('hit mount point, breaking')
            break
        source_folder = os.path.dirname(source_folder)

    for file in reversed(settings_files):
        with open(file) as stream:
            settings = update_nested_dict(settings, yaml.load(stream))
    LOGGER.info(f'settings:\n{pprint.pformat(settings)}')
    return settings


def _get_media_folders(source_folder: str) -> list:
    LOGGER.info('gathering media folders')

    media_folders = []

    while True:
        LOGGER.debug(f'traversing: {source_folder}')
        folder = os.path.join(source_folder, 'media')
        if os.path.exists(folder) and os.path.isdir(folder):
            LOGGER.info(f'media folder found: {folder}')
            media_folders.append(folder.replace('\\', '/'))
        if os.path.ismount(source_folder):
            LOGGER.debug('hit mount point, breaking')
            break
        source_folder = os.path.dirname(source_folder)

    LOGGER.info(f'media folders:\n{pprint.pformat(media_folders)}')
    return media_folders


def convert_source_folder(
        source_folder: str,
        keep_temp_dir: bool = False,
):

    LOGGER.info(f'converting to PDF: {source_folder}')

    temp_dir = _get_temp_folder()

    source_folder = ensure_folder_exists(source_folder)
    LOGGER.debug(f'source folder: {source_folder}')

    template_folder = _get_template_folder(source_folder)

    index_file = _get_index_file(source_folder)

    settings = _get_settings(source_folder)

    media_folders = _get_media_folders(source_folder)

    markdown = process_markdown(index_file, settings, media_folders)

    tex_template = process_template(
        template_file_='template.tex',
        template_folder_=template_folder,
        media_folders_=media_folders,
    )

    source_file = os.path.join(temp_dir, 'source.md')
    with open(source_file, 'w') as stream:
        stream.write(markdown)

    template_file = os.path.join(temp_dir, 'template.tex')
    with open(template_file, 'w', encoding='utf8') as stream:
        stream.write(tex_template)
        
    title = os.path.basename(source_folder)
    out_folder = './OUTPUT/PDF'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    out_file = os.path.join(out_folder, title + '.PDF')


    do(
        [
            'pandoc',
            '-s',
            '--toc',
            '--template', template_file,
            source_file,
            '-o',
            out_file,
            '-V', 'geometry:margin=2.5cm',
            '-V', 'lot',
            '-V', 'lof',
            '-V', 'colorlinks=true',
            '-V', 'papersize:a4',
            # '-V', f'title={title}',
            '-N',
        ],
    )

    if not keep_temp_dir:
        shutil.rmtree(temp_dir)


CONVERT = {
    'MD': {
        'PDF': convert_source_folder,
    },
}


class Convert:
    def __init__(self):
        pass

    @staticmethod
    def make_md(infile, outfile=None, outdir=None):

        if outfile is None:
            outfile = f'{os.path.splitext(infile)[0]}.md'

        if outdir is None:
            outdir = os.path.join(
                os.path.dirname(infile),
                os.path.splitext(os.path.basename(infile))[0],
            )

        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        os.makedirs(outdir)

        do(
            [
                'pandoc',
                '-s',
                f'--extract-media={outdir}',
                # '-S',
                # '-t', 'rst',
                infile,
                '-o',
                outfile,
                # '-V', 'geometry:margin=1in',
            ]
        )

    @staticmethod
    def _clean_pdf_latex_working_folders():
        LOGGER.debug(f'Cleaning pdflatex working directories in: {os.path.abspath(".")}')
        for temp_tex_folder in glob.glob('tex2pdf.*'):
            LOGGER.debug(f'removing: {temp_tex_folder}')
            shutil.rmtree(temp_tex_folder)

    # noinspection PyMethodMayBeStatic
    def make_pdf(self, infile, outfile=None, title=None, resources=None):
        LOGGER.debug(f'Making PDF from: {infile}')

        if outfile is None:
            outfile = f'{os.path.splitext(infile)[0]}.pdf'

        LOGGER.debug(f'Output file: {outfile}')

        if title is None:
            title = os.path.splitext(os.path.basename(infile))[0]

        LOGGER.debug(f'Document title: {title}')

        if resources is None:
            resources = os.path.splitext(infile)[0]

        LOGGER.debug(f'Resource directory: {resources}')

        do(
            [
                'pandoc',
                '-s',
                '--toc',
                '--template', './templates/template.tex',
                infile,
                '-o',
                outfile,
                '-V', 'geometry:margin=2.5cm',
                '-V', 'lot',
                '-V', 'lof',
                '-V', f'title={title}',
                '-N',
            ],
        )

        self._clean_pdf_latex_working_folders()
