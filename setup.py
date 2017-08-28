# coding=utf-8

from setuptools import setup, find_packages

install_requires = [
    'click',
    'certifi',
    'urllib3',
    'requests',
    'click_log',
    'jinja2',
    'pyyaml',
    'setuptools-scm',
]

test_requires = [
    'pytest',
    'pytest-pycharm',
    'pytest-pep8',
    'pytest-cache',
    'pytest-catchlog',
    'pytest-cov',
    'pytest-mock',
    'pytest-pep8',
    'coverage',
    'flake8',
    'pylint',
    'safety',
    'hypothesis',

]

dev_requires = [
    'pip-tools',
]

setup_requires = [
    'pytest-runner',
    'setuptools_scm',
]

entry_points = '''
[console_scripts]
edlm=edlm.cli:cli
'''


def main():
    setup(
        name='edlm',
        use_scm_version=True,
        install_requires=install_requires,
        entry_points=entry_points,
        tests_require=test_requires,
        setup_requires=setup_requires,
        test_suite='pytest',
        packages=find_packages('.'),
    )


if __name__ == '__main__':
    main()
