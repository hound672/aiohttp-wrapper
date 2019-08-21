import pytest

from aiohttp import web
from faker import Factory
from pydantic import BaseModel

from aiohttp_wrapper import init_aiohttp_wrapper

@pytest.fixture
def faker():
    """Faker object"""
    return Factory.create()

@pytest.fixture
async def app(loop):
    """Create main application"""

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
    return _app
