# coding=utf-8

import hashlib

import pdfrw
from pdfrw.objects import pdfstring

from edlm import __version__
from edlm.convert import Context


def _iterate_over_data(ctx: Context):
    yield ctx.index_file.read_bytes()
    yield ctx.template_source.read_bytes()
    for settings_file in ctx.settings_files:
        yield settings_file.read_bytes()
    for media_folder in ctx.media_folders:
        for file in media_folder.iterdir():
            yield file.read_bytes()


def _get_document_hash(ctx: Context) -> str:
    m = hashlib.md5()
    for data in _iterate_over_data(ctx):
        m.update(data)
    return m.hexdigest()


def skip_file(ctx: Context):
    if ctx.out_file.exists():
        pdf = pdfrw.PdfReader(str(ctx.out_file.absolute()))
        creator = pdfstring.PdfString.to_unicode(pdf.Info.Creator)
        if creator != 'EDLM ' + __version__:
            ctx.info('document generated with an older version of ELDM, regenerating')
            return False
        producer = pdfstring.PdfString.to_unicode(pdf.Info.Producer)
        if producer != 'EDLM ' + _get_document_hash(ctx):
            ctx.debug('document updated')
            return False
        ctx.info('this document has not been modified, skipping it')
        return True


def add_metadata_to_pdf(ctx: Context):
    out_file = str(ctx.out_file.absolute())
    trailer = pdfrw.PdfReader(out_file)
    trailer.Info.Author = '132nd-etcher'
    trailer.Info.Creator = 'EDLM ' + __version__
    trailer.Info.Producer = 'EDLM ' + _get_document_hash(ctx)
    pdfrw.PdfFileWriter(out_file, trailer=trailer).write()
