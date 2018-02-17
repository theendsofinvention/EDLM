# coding=utf-8

import pytest

from edlm.convert._context import Context, _Val


@pytest.mark.parametrize(
    'level',
    ['debug', 'info', 'warning', 'error']
)
def test_logger(caplog, level):
    caplog.clear()
    ctx = Context()
    func = getattr(ctx, level)
    assert 'test' not in caplog.text
    func('test')
    assert 'test' in caplog.text


def test_no_default():
    class Dummy(Context):
        no_default = _Val(str)

    dummy = Dummy()
    with pytest.raises(KeyError):
        _ = dummy.no_default


def test_wrong_type():
    ctx = Context()
    with pytest.raises(TypeError):
        ctx.title = 1
