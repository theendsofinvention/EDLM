# coding=utf-8
import os
import re

from edlm import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)

RE_PICTURE_LINE = re.compile(r'\!\['
                             r'(?P<caption>.*)'
                             r'\]'
                             r'\('
                             r'(?P<picture>.+)'
                             r'\)'
                             r'(?P<extras>.*)')


def _get_image_full_path(image: str, media_folders: list):
    image_name = os.path.basename(image)
    for folder in media_folders:
        path = os.path.abspath(os.path.join(folder, image_name))
        if os.path.exists(path):
            return path
    else:
        raise FileNotFoundError(f'picture "{image}" not found in any media folders: {media_folders}')


def process_images(content: str, settings: dict, media_folders: list):
    LOGGER.info('processing pictures')
    pictures_found = set()
    unused_pictures = set()
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
                LOGGER.debug(f'processing picture: {picture}')
                pictures_found.add(os.path.basename(picture))
                picture = _get_image_full_path(picture, media_folders)

                if not extras:
                    extras = f'{{width="{settings.get("default_pic_width", "10cm")}"}}'

                output.append(f'![{caption}]({picture}){extras}')

        else:
            output.append(line)

    if len(media_folders) > 1:
        LOGGER.debug('checking media path for unused pictures')
        for file in os.listdir(media_folders[0]):
            if file not in pictures_found:
                LOGGER.debug(f'checing that "{file}" is used')
                unused_pictures.add(file)

        if unused_pictures:
            unused_pictures = '\n\t'.join(sorted(unused_pictures))
            LOGGER.warning(f'unused files found:\n\t{unused_pictures}')

    LOGGER.info('processing of pictures finished')
    return '\n'.join(output)