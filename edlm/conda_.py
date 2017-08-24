# coding=utf-8

import json
from collections import namedtuple

from edlm.config import CFG
from edlm.utils import do

CondaPackage = namedtuple('CondaPackage',
                          ['base_url', 'build_number', 'build_string', 'channel', 'dist_name', 'name', 'platform',
                           'version', 'with_features_depends'])
CondaInstallResult = namedtuple('CondaInstall', ['actions', 'success', 'message', 'caused_by', 'channels', 'error', 'exception_name', 'exception_type', 'pkg'])


def conda_env() -> str:
    if CFG.conda_env:
        return f'-n {CFG.conda_env}'
    else:
        return ''


def conda_list() -> list:
    return json.loads(do(f'conda list {conda_env()} --json'))


def installed_packages():
    for package in conda_list():
        yield CondaPackage(**package)


def conda_install(package_name: str) -> CondaInstallResult:
    result = {
        'message': '',
        'actions': '',
        'caused_by': '',
        'channels': '',
        'error': '',
        'exception_name': '',
        'exception_type': '',
        'pkg': '',
        'success': '',
    }
    result.update(json.loads(do(f'conda install {conda_env()} --json {package_name}', exit_on_fail=False)))
    print(result.keys())
    return CondaInstallResult(**result)
    # return CondaInstallResult(**result)


if __name__ == '__main__':
    # print(CFG.debug)
    # print(CFG.conda_env)
    # for package in installed_packages():
    #     print(package.name)
    result = conda_install('pandoc miktex')
    if result.exception_name:
        raise RuntimeError(result.exception_name)
    if result.message:
        print(result.message)
    if result.success:
        print(result.success)
