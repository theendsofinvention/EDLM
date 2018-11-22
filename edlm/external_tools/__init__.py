# coding=utf-8
"""
EDLM external tools
"""

# noinspection PyProtectedMember
from edlm.external_tools.miktext._miktext import MikTex
# noinspection PyProtectedMember
from edlm.external_tools.pandoc._pandoc import Pandoc

MIKTEX = MikTex()
PANDOC = Pandoc()
