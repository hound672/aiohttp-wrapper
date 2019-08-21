import os
import asyncio

import yaml
from typing import Type, Optional, Coroutine, Any, Callable
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
                         start_up: Optional[Callable[[web.Application], Coroutine[Any, Any, None]]] = None,
                         env_config: str = 'CONFIG_FILE',
                         default_config_file: str = 'config.yml',
                         config_model: Optional[Type[BaseModel]] = None
                         ) -> web.Application:
    """
    Init aiohttp wrapper
    :param start_up: Coroutine for start up workflow
    :param env_config: env variable name for config file
    :param default_config_file: default config file name
    :param config_model: Pydantic's model for validate config
    :return:
    """
    app = web.Application()
    app.middlewares.append(middleware_error)

    # read settings
    if config_model is not None:
        config_file_name = os.environ.get(env_config, default_config_file)
        app['config'] = _read_config(config_file_name, config_model)

    # start up func
    if start_up is not None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_up(app))

    return app
