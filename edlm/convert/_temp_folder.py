# coding=utf-8
"""
Manages temporary folder
"""

import logging
import shutil
import tempfile

import elib

from edlm.convert._context import Context

LOGGER = logging.getLogger('EDLM')


class TempDir:
    """
    Manages temporary folder
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.path = elib.path.ensure_dir(tempfile.mkdtemp(dir='.', prefix='__TMP')).absolute()

    def __enter__(self):
        LOGGER.debug('"%s": using temporary folder: "%s"', self.ctx.source_folder, self.path)
        self.ctx.temp_dir = self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            if self.ctx.keep_temp_dir:
                LOGGER.info('"%s": build successful, keeping temp dir: "%s"', self.ctx.source_folder, self.path)
            else:
                LOGGER.debug('"%s": build successful, removing temp dir', self.ctx.source_folder)
                shutil.rmtree(str(self.path.absolute()))
                self.ctx.temp_dir = None
        else:
            LOGGER.warning('"%s": build failed, keeping temp dir: "%s"', self.ctx.source_folder, self.path)
