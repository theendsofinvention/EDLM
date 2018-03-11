# coding=utf-8

from pathlib import Path

from edlm.convert import Context
from edlm.convert._get_settings import get_settings

BASE_SETTINGS = r"""
# Some comment
aliases:
  //alia1: alia1
  //alia2: "alia2"
references:
  //ref1: ref1_name, ref1_url
  //ref2: "ref2_name, ref2_url"
  //ref3: 'ref3_name, ref3_url'
papersize:
  - a4
links:
  linkcolor: Grey
  citecolor: "Grey"
"""

UPDATE_SETTINGS = r"""
aliases:
  //alia1: alia1_mod
  //alia3: "alia3"
references:
  //ref3: 'ref3_name_mod, ref3_url_mod'
  //ref4: 'ref4_name, ref4_url'
papersize:
  - a4
  - a5
links:
  citecolor: "Black"
  anchorcolor: Green
"""


def test_get_settings():
    ctx = Context()

    ctx.source_folder = Path('.').absolute()
    Path('settings.yml').write_text(BASE_SETTINGS)
    get_settings(ctx)
    assert ctx.settings.aliases == {
        '//alia1': 'alia1',
        '//alia2': 'alia2',
    }
    assert ctx.settings.references == {
        '//ref1': 'ref1_name, ref1_url',
        '//ref2': 'ref2_name, ref2_url',
        '//ref3': 'ref3_name, ref3_url',
    }
    assert ctx.settings.papersize == ['a4']
    assert ctx.settings.links == {
        'linkcolor': 'Grey',
        'citecolor': 'Grey',
    }


def test_update_nested_settings():
    ctx = Context()
    ctx.source_folder = Path('sub').absolute()
    ctx.source_folder.mkdir()
    Path('settings.yml').write_text(BASE_SETTINGS)
    Path('sub/settings.yml').write_text(UPDATE_SETTINGS)
    get_settings(ctx)

    assert ctx.settings.aliases == {
        '//alia1': 'alia1_mod',
        '//alia2': 'alia2',
        '//alia3': 'alia3',
    }
    assert ctx.settings.references == {
        '//ref1': 'ref1_name, ref1_url',
        '//ref2': 'ref2_name, ref2_url',
        '//ref3': 'ref3_name_mod, ref3_url_mod',
        '//ref4': 'ref4_name, ref4_url',
    }
    assert ctx.settings.papersize == ['a4', 'a5']
    assert ctx.settings.links == {
        'linkcolor': 'Grey',
        'citecolor': 'Black',
        'anchorcolor': 'Green',
    }
