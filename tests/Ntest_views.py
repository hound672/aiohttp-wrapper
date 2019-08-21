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
async def client_test_mixin(app, aiohttp_client):
    app.add_routes([
        web.view('/index', _Index, name='index')
    ])
    client = await aiohttp_client(app)
    return client

########################################################

async def test_get_empty(client_test_mixin):
    res = await client_test_mixin.get('/index')
    data = await res.json()

    assert res.status == 200
    assert data == {}


async def test_wo_json(client_test_mixin):
    res = await client_test_mixin.post('/index')
    data = await res.json()

    assert res.status == 400
    assert data['reason'] == 'ERR_NO_JSON'

async def test_validate_data_fail(client_test_mixin, faker):
    req = {faker.word(): faker.word()}
    res = await client_test_mixin.post('/index', json=req)
    data = await res.json()

    assert res.status == 400
    assert data['reason'] == 'ERR_VALIDATION'


async def test_validate_data_success(client_test_mixin, faker):
    req = {'name': faker.word()}
    res = await client_test_mixin.post('/index', json=req)
    data = await res.json()

    assert res.status == 200
    assert data == {}
