# coding=utf-8

import elib
from mockito import when

from edlm import external_tools


def test_pandoc():
    pandoc = external_tools.Pandoc()
    pandoc._exe = 'exe'
    when(elib).run('exe --version', mute=True).thenReturn(('pandoc version\ntext', 0))
    assert pandoc.version == 'version'
    assert pandoc.version == 'version'