# coding=utf-8
"""
Manages ESST configuration
"""

import os

import everett
import everett.manager


class Config:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    Singleton configuration class for EDLM.
    """
    def __init__(self):
        self._config = everett.manager.ConfigManager(
            [

                everett.manager.ConfigEnvFileEnv('.env'),
                everett.manager.ConfigOSEnv(),
                everett.manager.ConfigIniEnv(
                    [
                        os.environ.get('EDLM_INI'),
                        os.path.join(os.path.expanduser('~'), 'edlm.ini'),
                        './edlm.ini',
                    ]
                ),
                everett.manager.ConfigDictEnv(
                    {
                        'DEBUG': 'false',
                        'CONDA_ENV': '',
                    }
                ),
            ]
        )

        self.debug = self._config('DEBUG', parser=everett.manager.parse_bool)
        self.conda_env = self._config('CONDA_ENV', parser=str)


try:
    CFG = Config()
except everett.InvalidValueError as exception:
    KEY = exception.key
    if exception.namespace:
        KEY = f'{exception.namespace}_{KEY}'
    print(f'Invalid value for key: {KEY}')
    exit(1)
except everett.ConfigurationMissingError as exception:
    KEY = exception.key
    if exception.namespace:
        KEY = f'{exception.namespace}_{KEY}'
    print(f'Missing configuration for key: {KEY}')
    exit(1)

__all__ = ['CFG']
