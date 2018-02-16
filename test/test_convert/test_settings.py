# coding=utf-8
from pathlib import Path
import pytest
from edlm.convert import Context, ConvertError
import edlm.convert._get_settings as settings


def test_update_nested_dict():
    source_dict = {
        'source': 'source',
        'shared': 'source',
        'sub': {
            'source': 'source',
            'shared': 'source',
        }
    }
    target_dict = {
        'target': 'target',
        'shared': 'target',
        'sub': {
            'target': 'target',
            'shared': 'target',
        }
    }
    settings.update_nested_dict(source_dict, target_dict)
    assert source_dict == {
        'source': 'source',
        'shared': 'target',
        'target': 'target',
        'sub': {
            'source': 'source',
            'shared': 'target',
            'target': 'target',
        }
    }


def test_no_setting_file():
    ctx = Context()
    ctx.source_folder = Path('.').absolute()
    with pytest.raises(ConvertError):
        settings.get_settings(ctx)


def test_single_settings():
    ctx = Context()
    ctx.source_folder = Path('.').absolute()
    settings_ = Path('./settings.yml')
    settings_.write_text('key: value')
    settings.get_settings(ctx)
    assert ctx.settings == {'key': 'value'}


def test_empty_settings():
    ctx = Context()
    ctx.source_folder = Path('.').absolute()
    settings_ = Path('./settings.yml')
    settings_.write_text('')
    with pytest.raises(ConvertError):
        settings.get_settings(ctx)


def test_nested_settings():
    sub1 = Path('./sub1').absolute()
    sub1.mkdir()
    settings_1 = Path(sub1, 'settings.yml').absolute()
    settings_1.write_text(
        'key1: value1\n'
        'key2: value1\n'
        'key3: value1\n'
        'key4:\n'
        '  key1: value1\n'
        '  key2: value1\n'
        '  key3: value1\n'
    )
    sub2 = Path(sub1, 'sub2').absolute()
    sub2.mkdir()
    settings_2 = Path(sub2, 'settings.yml').absolute()
    settings_2.write_text(
        'key2: value2\n'
        'key4:\n'
        '  key2: value2\n'
    )
    sub3 = Path(sub2, 'sub3').absolute()
    sub3.mkdir()
    settings_3 = Path(sub3, 'settings.yml').absolute()
    settings_3.write_text(
        'key3: value3\n'
        'key4:\n'
        '  key3: value3\n'
    )
    ctx = Context()
    ctx.source_folder = sub3
    settings.get_settings(ctx)
    assert ctx.settings == {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'key4': {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        },
    }
