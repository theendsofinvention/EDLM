# coding=utf-8
import re
from pathlib import Path

import elib

from .._context import Context

RE_PICTURE_LINE = re.compile(r'\!\['
                             r'(?P<caption>.*)'
                             r'\]'
                             r'\('
                             r'(?P<picture>.+)'
                             r'\)'
                             r'(?P<extras>.*)')

RE_WIDTH = re.compile(r'{width="(?P<width>.*)"}')
RE_WIDTH_RAW = re.compile(r'(?P<width>[\d]+)(?P<unit>.*)')


def _get_image_full_path(ctx: Context):
    image_name = Path(ctx.image).name
    for folder in ctx.media_folders:
        image_path = Path(folder, image_name)
        if image_path.exists():
            return image_path.absolute()
    else:
        raise FileNotFoundError(f'picture "{ctx.image}" not found in any media folders: {ctx.media_folders}')


def _get_correct_width(ctx: Context):
    match = RE_WIDTH_RAW.match(ctx.width_str)
    if not match:
        raise ValueError(ctx.width_str)

    width = int(match.group('width'))
    unit = match.group('unit')

    if unit == 'mm':
        pass
    elif unit == 'cm':
        width *= 10
    else:
        raise ValueError(unit)

    if width > ctx.max_image_width:
        ctx.debug(f'adapting width for "{ctx.image}" to {ctx.max_image_width}mm')
        ctx.width = ctx.max_image_width


def _process_image_width(ctx: Context):
    width_match = RE_WIDTH.match(ctx.extras)

    if width_match:
        ctx.width_str = width_match.group('width')
        _get_correct_width(ctx)
        return RE_WIDTH.sub(f'{{width="{ctx.width}mm"}}', ctx.extras)

    else:
        ctx.debug(f'setting default witdh for picture {ctx.image}')
        return f'{{width="{ctx.max_image_width}mm}}'


def process_images(ctx: Context):
    ctx.info('processing pictures')
    used_images = set()
    unused_images = set()
    output = []
    for line in ctx.markdown_text.split('\n'):
        match = RE_PICTURE_LINE.match(line)
        if match:
            ctx.caption = match.group('caption')
            ctx.image = match.group('picture')
            ctx.extras = match.group('extras')

            ctx.extras = _process_image_width(ctx)

            if ctx.image.startswith('http'):
                output.append(line)
            else:
                ctx.debug(f'processing picture: {ctx.image}')
                used_images.add(Path(ctx.image).name)
                ctx.image = _get_image_full_path(ctx)

                output.append(f'![{ctx.caption}]({ctx.image}){ctx.extras}')

        else:
            output.append(line)

    if len(ctx.media_folders) > 1:
        ctx.debug('checking media path for unused pictures')
        for file in Path(ctx.media_folders[0]).iterdir():
            if file.name not in used_images:
                ctx.debug(f'checking that "{file}" is used')
                unused_images.add(str(file.absolute()))

        if unused_images:
            ctx.warning(f'unused files found:\n{elib.pretty_format(sorted(unused_images))}')

    ctx.info('processing of pictures finished')
    ctx.markdown_text = '\n'.join(output)
