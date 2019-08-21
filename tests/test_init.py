from unittest.mock import patch

from pydantic import BaseModel
from aiohttp import web

from aiohttp_wrapper import init_aiohttp_wrapper

async def test_read_settings():

    # app settings
    class _DBSettings(BaseModel):
        host: str
        port: int

    class AppSettings(BaseModel):
        debug: bool
        database: _DBSettings

    _app = init_aiohttp_wrapper(
        default_config_file='./tests/data/test_config.yml',
        config_model=AppSettings
    )

    assert 'config' in _app
    config = _app['config'].dict()
    assert config == {'debug': True, 'database': {'host': 'some_host', 'port': 5555}}


def test_start_up(loop):
    async def _start_app(app: web.Application):
        app['was_called'] = True

    _app = init_aiohttp_wrapper(
                start_up=_start_app
            )
    assert 'was_called' in _app
    assert _app['was_called']
