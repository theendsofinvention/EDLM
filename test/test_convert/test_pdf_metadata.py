# coding=utf-8

from pathlib import Path
from mockito import when, verify, mock
import pdfrw
from pdfrw.objects import pdfstring

from edlm.convert import _pdf_info
from edlm import __version__


def test_get_document_hash():
    ctx = _pdf_info.Context()
    index_file = Path('index')
    index_file.write_text('dsfsdfsdfsdfsdf')
    template = Path('template')
    template.write_text('sxdvxfgsfdsdf')
    settings = Path('settings')
    settings.write_text('cxvsdfgqsdfqsdq')
    media = Path('./media')
    media.mkdir()
    pic = Path(media, 'pic')
    pic.write_text('sdvsdfsdfqazfqsdf')
    ctx.index_file = index_file
    ctx.template_source = template
    ctx.settings_files = [settings]
    ctx.media_folders = [media]
    hash_ = _pdf_info._get_document_hash(ctx)
    assert hash_ == _pdf_info._get_document_hash(ctx)
    index_file.write_text('sdfsfsaqzzdqscxdcg')
    assert hash_ != _pdf_info._get_document_hash(ctx)
    hash_ = _pdf_info._get_document_hash(ctx)
    assert hash_ == _pdf_info._get_document_hash(ctx)
    template.write_text('sdgfsdfqljkqslkjdh')
    assert hash_ != _pdf_info._get_document_hash(ctx)
    hash_ = _pdf_info._get_document_hash(ctx)
    assert hash_ == _pdf_info._get_document_hash(ctx)
    settings.write_text('sdgfsdfqljkqslkjdh')
    assert hash_ != _pdf_info._get_document_hash(ctx)
    hash_ = _pdf_info._get_document_hash(ctx)
    assert hash_ == _pdf_info._get_document_hash(ctx)
    pic.write_text('sdgfsdfqljkqslkjdh')
    assert hash_ != _pdf_info._get_document_hash(ctx)
    hash_ = _pdf_info._get_document_hash(ctx)
    assert hash_ == _pdf_info._get_document_hash(ctx)


def test_skip_file_doesnt_exist():
    ctx = _pdf_info.Context()
    ctx.out_file = Path('./test')
    assert not _pdf_info.skip_file(ctx)


def test_skip_file_should_skip(caplog):
    ctx = _pdf_info.Context()
    ctx.out_file = Path('./test')
    pdf = mock()
    pdf.Info = mock()
    pdf.Info.Creator = 'creator'
    pdf.Info.Producer = 'producer'
    Path('./test').touch()
    when(pdfrw).PdfReader(...).thenReturn(pdf)
    when(pdfrw.objects.pdfstring.PdfString).to_unicode(...)\
        .thenReturn('EDLM ' + __version__)\
        .thenReturn('EDLM hash')
    when(_pdf_info)._get_document_hash(...).thenReturn('hash')
    assert _pdf_info.skip_file(ctx)
    assert 'this document has not been modified, skipping it' in caplog.text


def test_skip_file_document_updated(caplog):
    ctx = _pdf_info.Context()
    ctx.out_file = Path('./test')
    pdf = mock()
    pdf.Info = mock()
    pdf.Info.Creator = 'creator'
    pdf.Info.Producer = 'producer'
    Path('./test').touch()
    when(pdfrw).PdfReader(...).thenReturn(pdf)
    when(pdfrw.objects.pdfstring.PdfString).to_unicode(...)\
        .thenReturn('EDLM ' + __version__)\
        .thenReturn('EDLM not the hash')
    when(_pdf_info)._get_document_hash(...).thenReturn('hash')
    assert not _pdf_info.skip_file(ctx)
    assert 'document updated, regenerating' in caplog.text


def test_skip_file_wrong_version(caplog):
    ctx = _pdf_info.Context()
    ctx.out_file = Path('./test')
    pdf = mock()
    pdf.Info = mock()
    pdf.Info.Creator = 'creator'
    pdf.Info.Producer = 'producer'
    Path('./test').touch()
    when(pdfrw).PdfReader(...).thenReturn(pdf)
    when(pdfrw.objects.pdfstring.PdfString).to_unicode(...)\
        .thenReturn('EDLM wrong version')\
        .thenReturn('EDLM hash')
    when(_pdf_info)._get_document_hash(...).thenReturn('hash')
    assert not _pdf_info.skip_file(ctx)
    assert 'document generated with an older version of EDLM, regenerating' in caplog.text


def test_add_metadata():
    ctx = _pdf_info.Context()
    ctx.out_file = Path('./test')
    Path('./test').touch()
    writer = mock()
    when(writer).write()
    trailer = mock()
    trailer.Info = mock()
    when(pdfrw).PdfReader(str(ctx.out_file.absolute())).thenReturn(trailer)
    when(pdfrw).PdfFileWriter(str(ctx.out_file.absolute()), trailer=trailer).thenReturn(writer)
    when(_pdf_info)._get_document_hash(...).thenReturn('hash')
    _pdf_info.add_metadata_to_pdf(ctx)
    verify(writer).write()
    assert trailer.Info.Creator == 'EDLM ' + __version__
    assert trailer.Info.Producer == 'EDLM hash'
