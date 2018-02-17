# coding=utf-8

import pytest

from edlm.convert._context import Context


@pytest.mark.parametrize(
    'level',
    ['debug', 'info', 'warning', 'error']
)
def test_logger(caplog, level):
    caplog.clear()
    ctx = Context()
    print(ctx.source_folder)
    func = getattr(ctx, level)
    assert 'test' not in caplog.text
    func('test')
    assert 'test' in caplog.text
