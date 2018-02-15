# coding=utf-8

import pytest
import click
from click.testing import CliRunner
from old_convert.main import cli


def test_basic(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert 'Usage: cli [OPTIONS] COMMAND [ARGS]...' in result.output
