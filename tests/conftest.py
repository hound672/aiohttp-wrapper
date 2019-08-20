import pytest

from aiohttp import web
from faker import Factory

from aiohttp_wrapper import init_aiohttp_wrapper

@pytest.fixture
def faker():
    """Faker object"""
    return Factory.create()

@pytest.fixture
async def app(loop):
    """Create main application"""
    _app = web.Application()
    await init_aiohttp_wrapper(_app)
    return _app
