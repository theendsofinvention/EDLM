# coding=utf-8

# coding=utf-8
import os
import shlex
import subprocess
import sys
import typing

import click

from edlm import MAIN_LOGGER

LOGGER = MAIN_LOGGER.getChild(__name__)


def find_executable(executable: str, path: str = None) -> typing.Union[str, None]:  # noqa: C901
    # noinspection SpellCheckingInspection
    """
    https://gist.github.com/4368898

    Public domain code by anatoly techtonik <techtonik@gmail.com>

    Programmatic equivalent to Linux `which` and Windows `where`

    Find if ´executable´ can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.

    Args:
        executable: executable name to look for
        path: root path to examine (defaults to system PATH)

    """

    # if not executable.endswith('.exe'):
    #     executable = f'{executable}.exe'

    if executable in find_executable.known_executables:  # type: ignore
        return find_executable.known_executables[executable]  # type: ignore

    click.secho(f'looking for executable: {executable}', fg='green', nl=False)

    if path is None:
        path = os.environ['PATH']
    paths = [
                os.path.abspath('.'),
                os.path.abspath(os.path.join(sys.exec_prefix, 'Scripts'))
            ] + path.split(os.pathsep)

    for path_ in paths:
        for ext in ['.exe']:
            executable_path = os.path.join(path_, executable + ext)
            if os.path.isfile(executable_path):
                find_executable.known_executables[executable] = executable_path
                click.secho(f' -> {click.format_filename(executable_path)}', fg='green')
                return executable_path
    else:
        click.secho(f' -> not found', fg='red', err=True)
        return None


find_executable.known_executables = {}


def do_ex(cmd: typing.List[str], cwd: str = '.') -> typing.Tuple[str, str, int]:
    """
    Executes a given command

    Args:
        cmd: command to run
        cwd: working directory (defaults to ".")

    Returns: stdout, stderr, exit_code

    """

    def _popen_pipes(cmd_, cwd_):
        def _always_strings(env_dict):
            """
            On Windows and Python 2, environment dictionaries must be strings
            and not unicode.
            """
            env_dict.update(
                (key, str(value))
                for (key, value) in env_dict.items()
            )
            return env_dict

        return subprocess.Popen(
            cmd_,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(cwd_),
            env=_always_strings(
                dict(
                    os.environ,
                    # try to disable i18n
                    LC_ALL='C',
                    LANGUAGE='',
                    HGPLAIN='1',
                )
            )
        )

    def _ensure_stripped_str(str_or_bytes):
        if isinstance(str_or_bytes, str):
            return '\n'.join(str_or_bytes.strip().splitlines())
        return '\n'.join(str_or_bytes.decode('utf-8', 'surogate_escape').strip().splitlines())

    exe = find_executable(cmd.pop(0))
    if not exe:
        exit(-1)
    cmd.insert(0, exe)
    click.secho(f'{cmd}', nl=False, fg='magenta')
    pipe = _popen_pipes(cmd, cwd)
    out, err = pipe.communicate()
    click.secho(f' -> {pipe.returncode}', fg='magenta')
    return _ensure_stripped_str(out), _ensure_stripped_str(err), pipe.returncode


def do(cmd, cwd: str = '.', exit_on_fail=True) -> str:  # pylint: disable=invalid-name
    """
    Executes a command and returns the result

    Args:
        cmd: command to execute
        cwd: working directory (defaults to ".")

    Returns: stdout
    """
    if not isinstance(cmd, (list, tuple)):
        cmd = shlex.split(cmd)

    out, err, ret = do_ex(cmd, cwd)
    if out:
        LOGGER.debug(out)
        click.secho(out, fg='green')
    if err:
        LOGGER.error(err)
        click.secho(err, fg='red', err=True)
    if ret:
        LOGGER.error(f'command failed: {cmd}')
        click.secho(f'command failed: {cmd}', fg='red', err=True)
        if exit_on_fail:
            exit(ret)
    return out
