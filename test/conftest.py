# coding=utf-8

import os

import pytest
from click.testing import CliRunner


@pytest.fixture(scope='session')
def miktex_path():
    yield os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            'miktex',
        )
    )


@pytest.fixture()
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner
