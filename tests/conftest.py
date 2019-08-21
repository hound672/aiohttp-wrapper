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

    _app = init_aiohttp_wrapper()
    return _app
