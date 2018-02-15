# coding=utf-8

import elib


class Config(elib.config.BaseConfig):

    def __init__(self):
        elib.config.BaseConfig.__init__(self, __package__)

    @elib.config.ConfigProp(str, default='./miktex.7z')
    def miktex_archive(self):
        pass

    @elib.config.ConfigProp(str, default='./miktex')
    def miktex_path(self):
        pass

    @elib.config.ConfigProp(str, default='./pandoc.7z')
    def pandoc_archive(self):
        pass

    @elib.config.ConfigProp(str, default='./pandoc')
    def pandoc_path(self):
        pass

    @elib.config.ConfigProp(parser=bool, default=False)
    def debug(self):
        pass


config = Config()
