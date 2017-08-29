# coding=utf-8
import os
import re
from edlm import MAIN_LOGGER
from edlm.utils import ensure_file_exists, ensure_folder_exists
from collections import namedtuple
from jinja2 import Environment, Template, FileSystemLoader


LOGGER = MAIN_LOGGER.getChild(__name__)

RE_PICTURE_LINE = re.compile(r'\!\['
                             r'(?P<caption>.*)'
                             r'\]'
                             r'\('
                             r'(?P<picture>.+)'
                             r'\)'
                             r'(?P<extras>.*)')

def _process_aliases(content: str, settings: dict) -> str:
    LOGGER.debug('processing aliases')
    for alias, value in settings.get('aliases', {}).items():
        LOGGER.debug(f'processing alias: {alias}')
        content = content.replace(alias, value)
    return content


def _get_image_full_path(image: str, media_folders: list):
    image_name = os.path.basename(image)
    for folder in media_folders:
        path = os.path.abspath(os.path.join(folder, image_name))
        if os.path.exists(path):
            return path
    else:
        raise FileNotFoundError(f'picture "{image}" not found in any media folders: {media_folders}')


def _process_images(content: str, settings: dict, media_folders: list):
    output = []
    for line in content.split('\n'):
        match = RE_PICTURE_LINE.match(line)
        if match:
            caption = match.group('caption')
            picture = match.group('picture')
            extras = match.group('extras')

            if picture.startswith('http'):
                output.append(line)
            else:
                picture = _get_image_full_path(picture, media_folders)

                if not extras:
                    extras = f'{{width="{settings.get("default_pic_width", "10cm")}"}}'

                output.append(f'![{caption}]({picture}){extras}')

        else:
            output.append(line)

    return '\n'.join(output)


def process_markdown(markdown_file: str, settings: dict, media_folders: list) -> str:
    markdown_file = ensure_file_exists(markdown_file)
    LOGGER.debug(f'processing markdown file: {markdown_file}')
    with open(markdown_file) as stream:
        content = stream.read()
    content = _process_aliases(content, settings)
    content = _process_images(content, settings, media_folders)
    return content


TEMPLATE_SETTINGS = namedtuple('TemplateSettings', ['media_dir_main', 'media_dir'])

def _get_jinja_env(template_dir: str):
    return Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(template_dir)
    )


def process_template(template_file_: str,
                     template_folder_: str,
                     media_folders_: list,
                     ) -> str:
    LOGGER.debug(f'processing template file: {template_file_}')

    template_dir = ensure_folder_exists(template_folder_)
    jinja_env = _get_jinja_env(template_folder_)

    media_folders = ''.join(f'{{{folder}/}}' for folder in media_folders_)
    # for folder in media_folders_:
    #     media_folders = media_folders + f'{{{folder}/}}'
    LOGGER.debug(f'adding media folders to template: {media_folders}')

    template = jinja_env.get_template(template_file_)
    return template.render(**locals())

