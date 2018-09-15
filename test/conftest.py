# coding=utf-8
"""
Pytest config
"""

import os
import sys

import pytest
from mockito import unstub


# noinspection PyUnusedLocal
def pytest_configure(config):
    """Setup"""
    assert config
    sys.called_from_test = True
    sys.path.append('.')


def pytest_unconfigure(config):
    """Tear down"""
    # noinspection PyUnresolvedReferences
    del sys.called_from_test
    assert config
    sys.path.remove('.')


@pytest.fixture(autouse=True)
def cleandir(request, tmpdir):
    """Provides a clean working dir"""
    if 'nocleandir' in request.keywords:
        yield
    else:
        current_dir = os.getcwd()
        os.chdir(str(tmpdir))
        yield os.getcwd()
        os.chdir(current_dir)


@pytest.fixture(autouse=True)
def _unstub():
    unstub()
    yield
    unstub()


@pytest.fixture(autouse=True)
def _reset_cache():
    from edlm.external_tools.base import _find_patool
    _find_patool.cache_clear()
    yield
    _find_patool.cache_clear()


@pytest.fixture(autouse=True)
def _setup_config():
    from edlm.config import CFG
    CFG.keep_temp_dir = False
    CFG.debug = False
    yield


def pytest_addoption(parser):
    """Add option for long tests"""
    parser.addoption("--long", action="store_true",
                     help="run long tests")


def pytest_runtest_setup(item):
    """Skip long tests"""
    long_marker = item.get_marker("long")
    if long_marker is not None and not item.config.getoption('long'):
        pytest.skip('skipping long tests')

@pytest.fixture()
def dummy_front_matter():
    yield """---
title: dummy_title
qualifier_short: dummy_qualifier_short
qualifier: dummy_qualifier
type: dummy_type
category: dummy_category 
title_pictures: dummy_title_pictures
header_picture: dummy_header_picture
description: dummy_description
opr: dummy_opr
certified_by:
  - dummy
supersedes:
  - dummy
link: dummy
published_date: dummy
summary_of_changes:
  - dummy
---
"""
