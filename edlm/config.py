# coding=utf-8
"""
Manages ESST configuration
"""

import os
import yaml

import everett
import everett.manager


class YAMLConfig:

    def __init__(self, possible_paths):
        self.cfg = {}
        possible_paths = everett.manager.listify(possible_paths)

        for path in possible_paths:
            if not path:
                continue

            path = os.path.abspath(os.path.expanduser(path.strip()))
            if path and os.path.isfile(path):
                self.cfg.update(self.parse_yaml_file(path))

        print(self.cfg)

    @staticmethod
    def parse_yaml_file(path: str):
        with open(path) as stream:
            return yaml.load(stream)

    def get(self, key, namespace=None):
        return str(everett.manager.get_key_from_envs(self.cfg, key, namespace))



class EverettConfig:

    def __init__(self, package_name: str, default_dict: dict = None):
        if default_dict is None:
            default_dict = {}
        self._config = everett.manager.ConfigManager(
            [
                everett.manager.ConfigEnvFileEnv('.env'),
                everett.manager.ConfigOSEnv(),
                YAMLConfig(
                    [
                        os.environ.get(f'{package_name.upper()}_YAML'),
                        os.path.join(os.path.expanduser('~'), f'{package_name}.yml'),
                        os.path.join(os.path.expanduser('~'), f'{package_name}.yaml'),
                        f'./{package_name}.yml',
                        f'./{package_name}.yaml',
                    ]
                ),
                everett.manager.ConfigIniEnv(
                    [
                        os.environ.get(f'{package_name.upper()}_INI'),
                        os.path.join(os.path.expanduser('~'), f'{package_name}.ini'),
                        f'./{package_name}.ini',
                    ]
                ),
                everett.manager.ConfigDictEnv(default_dict),
            ]
        )


class Config(EverettConfig):  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    Singleton configuration class for EDLM.
    """
    def __init__(self):
        default_dict = {
            'DEBUG': 'false',
            'CONDA_ENV': '',
        }
        EverettConfig.__init__(self, 'edlm', default_dict)
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
