# coding=utf-8

import collections
from pathlib import Path

import elib
import yaml

from ._context import Context


def update_nested_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update_nested_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def get_settings(ctx: Context):
    ctx.info('reading settings')

    settings = {}
    settings_files = []

    this_folder = ctx.source_folder
    while True:
        ctx.debug(f'traversing: {this_folder}')
        file = Path(this_folder, 'settings.yml')
        if file.exists() and file.is_file():
            ctx.debug(f'settings file found: {file}')
            settings_files.append(file)
        if len(this_folder.parents) is 1:
            ctx.debug(f'reach mount point at: "{this_folder}"')
            break
        this_folder = this_folder.parent

    for file in reversed(settings_files):
        with open(file) as stream:
            settings = update_nested_dict(settings, yaml.load(stream))
    ctx.debug(f'settings:\n{elib.pretty_format(settings)}')
    ctx.settings = settings
