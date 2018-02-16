# coding=utf-8

from mockito import when, verify, patch, mock, verifyStubbedInvocationsAreUsed
from edlm.external_tools.base import _find_patool, BaseExternalTool
import edlm.external_tools.base
import pyunpack
import copy
import sys
import elib
import pytest
from pathlib import Path


def test_find_patool_not_found():
    with pytest.raises(FileNotFoundError):
        _find_patool('.')


def test_patool_alongside():
    dummy = Path('dummy').absolute()
    patool = Path('patool').absolute()
    patool.touch()
    assert _find_patool(dummy) == patool


def test_patool_in_scripts_folder():
    scripts = Path('./scripts').absolute()
    scripts.mkdir()
    dummy = Path('dummy').absolute()
    patool = Path(scripts, 'patool').absolute()
    patool.touch()
    assert _find_patool(dummy) == patool
    patool.unlink()
    with pytest.raises(FileNotFoundError):
        _find_patool(dummy)



class Sub(BaseExternalTool):
    url = 'None'
    hash = 'None'
    default_archive = 'None'
    default_install = 'None'
    expected_version = 'None'

    @property
    def exe(self):
        return self._exe

    @property
    def version(self):
        return 'version'


def test_base_empty_init():

    sub = Sub()
    assert sub.url == 'None'
    assert sub.hash == 'None'
    assert sub.archive == Path('None').absolute()
    assert sub.install_dir == Path('None').absolute()
    assert sub.expected_version == 'None'


def test_base_meaningful_init():

    sub = Sub('archive', 'install_dir')
    assert sub.url == 'None'
    assert sub.hash == 'None'
    assert sub.archive == Path('archive').absolute()
    assert sub.install_dir == Path('install_dir').absolute()
    assert sub.expected_version == 'None'


def test_call():
    filters = None
    cwd = 'cwd'
    failure_ok = False
    cmd = 'some command'
    mute = False
    when(elib).run('test some command', cwd=cwd, mute=mute, filters=filters, failure_ok=failure_ok)\
        .thenReturn(('out', None))
    sub = Sub()
    exe = mock()
    when(exe).absolute().thenReturn('test')
    sub._exe = exe
    assert sub(cmd=cmd, cwd=cwd, mute=mute, filters=filters, failure_ok=failure_ok) == 'out'
    verifyStubbedInvocationsAreUsed()


@pytest.mark.parametrize(
    'attrib',
    ('default_install', 'default_archive', 'url', 'hash', 'expected_version')
)
def test_check_values(attrib):
    class Dummy(Sub):
        pass
    setattr(Dummy, attrib, None)
    with pytest.raises(ValueError):
        Dummy()


def test_archive_exists():
    sub = Sub()
    assert sub._archive_exists() is False
    archive = Path('./archive')
    archive.touch()
    sub.archive = archive
    assert sub._archive_exists() is True


def test_archive_is_correct():
    sub = Sub()
    assert sub._archive_is_correct() is False
    archive = Path('./archive')
    archive.touch()
    sub.archive = archive
    assert sub._archive_is_correct() is False
    sub.hash = elib.hash_.get_hash(archive.read_bytes())
    assert sub._archive_is_correct() is True


def test_archive_is_installed():
    sub = Sub()
    archive = Path('./archive')
    archive.touch()
    sub.archive = archive
    exe = Path('./exe')
    sub._exe = exe
    sub.archive = archive
    sub.hash = elib.hash_.get_hash(archive.read_bytes())
    assert sub._is_installed() is False
    exe.touch()
    assert sub._is_installed() is False
    sub.expected_version = 'version'
    assert sub._is_installed() is True


def test_download():
    when(elib.downloader).download(...).thenReturn(True)
    sub = Sub()
    assert sub._download() is True
    verify(elib.downloader).download(...)


def test_download_already_correct():
    when(elib.downloader).download(...).thenReturn(True)
    sub = Sub()
    archive = Path('./archive')
    archive.touch()
    sub.archive = archive
    exe = Path('./exe')
    sub._exe = exe
    sub.archive = archive
    sub.hash = elib.hash_.get_hash(archive.read_bytes())
    assert sub._download() is True
    verify(elib.downloader, times=0).download(...)


def test_download_failed():
    when(elib.downloader).download(...).thenReturn(False)
    sub = Sub()
    with pytest.raises(SystemExit):
        sub._download()


def test_extract():
    when(edlm.external_tools.base)._find_patool().thenReturn('patool')
    sub = Sub()
    archive = Path('./archive')
    archive.touch()
    sub.archive = archive
    exe = Path('./exe')
    sub._exe = exe
    sub.archive = archive
    sub.hash = elib.hash_.get_hash(archive.read_bytes())
    when(pyunpack.Archive).extractall(...)
    sub._extract()
    verify(pyunpack.Archive).extractall(...)


def test_setup():
    when(BaseExternalTool)._download()
    when(BaseExternalTool)._extract()
    sub = Sub()
    exe = Path('./exe')
    sub._exe = exe
    sub.setup()
    verify(BaseExternalTool)._download()
    verify(BaseExternalTool)._extract()
    archive = Path('./archive')
    archive.touch()
    sub.archive = archive
    sub.archive = archive
    sub.hash = elib.hash_.get_hash(archive.read_bytes())
    assert sub._is_installed() is False
    exe.touch()
    assert sub._is_installed() is False
    sub.expected_version = 'version'
    sub.setup()
    verify(BaseExternalTool)._download()
    verify(BaseExternalTool)._extract()



