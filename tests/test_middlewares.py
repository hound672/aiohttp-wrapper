import pytest

from aiohttp import web, web_exceptions

from aiohttp_wrapper import exceptions as wrapper_exceptions

########################################################

class _Success(web.View):
    async def get(self):
        return web.json_response({'result': 'ok'})

class _AiohttpExceptions(web.View):
    async def get(self):
        raise web_exceptions.HTTPBadRequest

class _WrapperException(web.View):
    async def get(self):
        raise wrapper_exceptions.HttpBadRequest({
            'error_1': 'describe_1',
            'error_2': 'describe_2'
        })

@pytest.fixture
async def client_middleware(app, aiohttp_client):
    app.add_routes([
        web.view('/success', _Success, name='success'),
        web.view('/aiohttp-exception', _AiohttpExceptions, name='aiohttp-exception'),
        web.view('/wrapper-exception', _WrapperException, name='wrapper-exception')
    ])
    client = await aiohttp_client(app)
    return client


########################################################

async def test_aiohttp_success(client_middleware):
    res = await client_middleware.get('/success')
    data = await res.json()
    assert data == {'result': 'ok'}
    assert res.status == 200

async def test_aiohttp_exception(client_middleware):
    res = await client_middleware.get('/aiohttp-exception')
    data = await res.json()
    assert res.status == 400
    assert data['reason'] == 'ERR_BAD_REQUEST'

async def test_wrapper_exception(client_middleware):
    res = await client_middleware.get('/wrapper-exception')
    data = await res.json()
    assert res.status == 400
    assert data['details'] == {'error_1': 'describe_1', 'error_2': 'describe_2'}

