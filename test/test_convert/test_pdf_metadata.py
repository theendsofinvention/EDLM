# coding=utf-8

from pathlib import Path

from edlm.convert import _pdf_info


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
