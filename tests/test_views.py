import pytest
from aiohttp import web
from pydantic import BaseModel

from aiohttp_wrapper.views import ValidateView


########################################################


class IndexPort(BaseModel):
    name: str

class _Index(ValidateView):
    post_body = IndexPort

    async def get(self):
        return web.json_response({})

    async def post(self):
        return web.json_response({})

@pytest.fixture
async def app_test_view(loop):
    """Create app for test view"""
    app = web.Application()
    app.add_routes([
        web.view('/index', _Index, name='index')
    ])
    return app


@pytest.fixture
async def client_test_mixin(app_test_view, aiohttp_client):
    client = await aiohttp_client(app_test_view)
    return client

########################################################

async def test_get_empty(client_test_mixin):
    res = await client_test_mixin.get('/index')
    data = await res.json()
    assert data == {}


async def test_post_validate(client_test_mixin):
    # res = await client_test_mixin.post('/index', json={'1':'2'})
    res = await client_test_mixin.post('/index')
    data = await res.text()
    pass

