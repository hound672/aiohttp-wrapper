import os

import yaml
from typing import Type
from aiohttp import web
from pydantic import BaseModel
from yaml import CLoader as Loader

from .middlewares import middleware_error


def _read_config(config_file_name: str,
                 config_model: Type[BaseModel]) -> BaseModel:
    """Read config from yml file"""
    with open(config_file_name, 'r') as fp:
        config = yaml.load(fp, Loader=Loader)
    return config_model(**config)

def init_aiohttp_wrapper(*,
                         env_config: str = 'CONFIG_FILE',
                         default_config_file: str = 'config.yml',
                         config_model: Type[BaseModel]
                         ) -> web.Application:
    """
    Init aiohttp wrapper
    :param env_config: env variable name for config file
    :param default_config_file: default config file name
    :param config_model: Pydantic's model for validate config
    :return:
    """
    app = web.Application()
    app.middlewares.append(middleware_error)

    # read settings
    config_file_name = os.environ.get(env_config, default_config_file)
    app['config'] = _read_config(config_file_name, config_model)

    return app
