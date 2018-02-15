# coding=utf-8
"""
Processes symbols
"""

from .._context import Context

SYMBOLS = {
    '°': r'\textdegree',
    '1/2': r'\textonehalf'
}


def process_symbols(ctx: Context):
    """
    Processes symbols
    """
    ctx.debug('processing symbols')
    for symbol in SYMBOLS:
        ctx.markdown_text = ctx.markdown_text.replace(
            symbol,
            f'{SYMBOLS[symbol]} ',
        )
