# coding=utf-8
"""
EDLM external tools
"""

from .miktext._miktext import MikTex
from .pandoc._pandoc import Pandoc


MIKTEX = MikTex()
PANDOC = Pandoc()
