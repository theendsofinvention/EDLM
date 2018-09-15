# coding=utf-8
"""
EDLM setup file
"""

from setuptools import find_packages, setup

requirements = [
    'certifi',
    'chardet',
    'click-log',
    'click',
    'idna',
    'jinja2',
    'markupsafe',
    'requests',
    'urllib3',
    'elib',
    'tqdm',
    'pyunpack',
    'patool',
    'pdfrw',
    'elib-run',
]
test_requirements = [
    'epab',
]

CLASSIFIERS = filter(None, map(str.strip,
                               """
Development Status :: 2 - Pre-Alpha
Environment :: Console
Environment :: Win32 (MS Windows)
Intended Audience :: End Users/Desktop
Natural Language :: English
Operating System :: Microsoft :: Windows :: Windows 7
Operating System :: Microsoft :: Windows :: Windows 8
Operating System :: Microsoft :: Windows :: Windows 8.1
Operating System :: Microsoft :: Windows :: Windows 10
License :: OSI Approved :: MIT License
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Documentation
Topic :: Text Processing
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: LaTeX
Topic :: Utilities
""".splitlines()))

entry_points = '''
[console_scripts]
edlm=edlm.__main__:main
'''

setup(
    name='EDLM',
    use_scm_version=True,
    install_requires=requirements,
    tests_require=test_requirements,
    entry_points=entry_points,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    python_requires='>=3.6',
    license='MIT',
    classifiers=CLASSIFIERS,
)
