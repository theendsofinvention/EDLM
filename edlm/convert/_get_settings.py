# coding=utf-8
"""
Gathers settings
"""

import collections
from pathlib import Path

import elib
import yaml

from ._context import Context
from ._exc import ConvertError


def update_nested_dict(source_dict, updated_dict):
    """
    Updates a dictionary from another

    Args:
        source_dict: source dictionary (will be overwritten)
        updated_dict: updated dictionary (will take precedence)

    Returns: merged dictionary

    """
    for key, value in updated_dict.items():
        if isinstance(value, collections.Mapping):
            result = update_nested_dict(source_dict.get(key, {}), value)
            source_dict[key] = result
        else:
            source_dict[key] = updated_dict[key]
    return source_dict


def get_settings(ctx: Context):
    """
    Gathers settings
    """
    ctx.info('reading settings')

    ctx.settings = {}
    ctx.settings_files = []

    this_folder = ctx.source_folder
    while True:
        ctx.debug(f'traversing: {this_folder}')
        file = Path(this_folder, 'settings.yml')
        if file.exists() and file.is_file():
            ctx.debug(f'settings file found: {file}')
            ctx.settings_files.append(file)
        if len(this_folder.parents) is 1:
            ctx.debug(f'reach mount point at: "{this_folder}"')
            break
        this_folder = this_folder.parent

    if not ctx.settings_files:
        raise ConvertError('no "settings.yml" file found', ctx)

    for file in reversed(ctx.settings_files):
        if not file.read_text():
            raise ConvertError(f'empty "settings.yml": {file.absolute()}', ctx)
        with open(file) as stream:
            update_nested_dict(ctx.settings, yaml.load(stream))
    ctx.debug(f'settings files:\n{elib.pretty_format(ctx.settings_files)}')
    ctx.debug(f'settings:\n{elib.pretty_format(ctx.settings)}')
