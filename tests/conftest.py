import pytest

from aiohttp import web

from aiohttp_wrapper import init_aiohttp_wrapper

@pytest.fixture
async def app(loop):
    """Create main application"""
    _app = web.Application()
    await init_aiohttp_wrapper(_app)
    return _app
