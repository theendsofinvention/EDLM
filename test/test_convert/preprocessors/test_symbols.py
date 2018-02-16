# coding=utf-8


from edlm.convert import Context
from edlm.convert._preprocessor import _symbols


def test_processing_symbols():
    ctx = Context()
    ctx.markdown_text = 'Some ° random 1/2 text'
    _symbols.process_symbols(ctx)
    assert ctx.markdown_text == r'Some \textdegree  random \textonehalf  text'
