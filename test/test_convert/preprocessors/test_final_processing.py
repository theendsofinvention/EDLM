# coding=utf-8

from pathlib import Path
from edlm.convert._preprocessor import _final_processing


def test_final_processing():
    ctx = _final_processing.Context()
    ctx.markdown_text = r'\command  text'
    _final_processing.final_processing(ctx)
    assert ctx.markdown_text == r'\command text'
