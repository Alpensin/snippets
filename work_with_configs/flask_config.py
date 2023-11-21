import os
import importlib
import json
from distutils.util import strtobool


def get_config(default_config='api.config'):
    config_module_path = os.getenv('CONFIG', default=default_config)
    try:
        config_module = importlib.import_module(config_module_path)
    except ImportError:
        print('error config import')
        raise

    env_prefix = getattr(config_module, 'ENV_PREFIX', '')

    for key, val in config_module.__dict__.items():
        if key.startswith('__'):
            continue

        env_val = os.getenv(f'{env_prefix}{key}')

        if not env_val:
            continue

        val_type = type(val)

        if val_type is bool:
            setattr(config_module, key, bool(strtobool(env_val)))
        elif val_type is str:
            setattr(config_module, key, env_val)
        elif val_type is dict:
            setattr(config_module, key, json.loads(env_val))
        else:
            setattr(config_module, key, val_type(env_val))

    return config_module

