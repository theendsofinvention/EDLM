# coding=utf-8
"""
Convert package exceptions
"""

from edlm.convert._context import Context


class ConvertError(Exception):
    """
    Raised when an error happen during the conversion
    """

    def __init__(self, message, ctx: Context) -> None:
        super(ConvertError, self).__init__(f'"{ctx.source_folder}": conversion error: {message}')
        self.ctx = ctx
