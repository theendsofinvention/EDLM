# coding=utf-8

from edlm.convert._settings import Settings


BASE_DICT = {
    'title': 'title',
    'papersize': ['a3', 'a4'],
    'aliases': {
        'alia1': 'alia1',
        'alia2': 'alia2',
        'alia3': 'alia3',
    },
    'references': {
        'ref1': ('ref1_name', 'ref1_url'),
        'ref2': ('ref2_name', 'ref2_url'),
    },
    'links': {
        'breaklinks': 'true',
        'bookmarks': 'true',
    }
}

UPDATE_DICT = {
    'papersize': ['a4'],
    'aliases': {
        'alia1': 'alia1_mod',
        'alia4': 'alia4',
    },
    'references': {
        'ref3': ('ref3_name', 'ref3_url'),
    },
    'links': {
        'breaklinks': 'false',
        'anchorcolor': 'Black',
    }
}


def test_simple_settings():
    settings = Settings()
    settings.update(BASE_DICT)
    assert settings.title == 'title'
    assert settings.papersize == ['a3', 'a4']
    assert settings.aliases == {
        'alia1': 'alia1',
        'alia2': 'alia2',
        'alia3': 'alia3',
    }
    assert settings.references == {
        'ref1': ('ref1_name', 'ref1_url'),
        'ref2': ('ref2_name', 'ref2_url'),
    }
    assert settings.links == {
        'breaklinks': 'true',
        'bookmarks': 'true',
    }


def test_simple_settings_update():
    settings = Settings()
    settings.update(BASE_DICT)
    settings.update(UPDATE_DICT)
    assert settings.title == 'title'
    assert settings.papersize == ['a4']
    assert settings.aliases == {
        'alia1': 'alia1_mod',
        'alia2': 'alia2',
        'alia3': 'alia3',
        'alia4': 'alia4',
    }
    assert settings.references == {
        'ref1': ('ref1_name', 'ref1_url'),
        'ref2': ('ref2_name', 'ref2_url'),
        'ref3': ('ref3_name', 'ref3_url'),
    }
    assert settings.links == {
        'breaklinks': 'false',
        'bookmarks': 'true',
        'anchorcolor': 'Black',
    }


