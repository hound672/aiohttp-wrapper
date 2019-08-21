async def test_read_settings(app):
    assert 'config' in app
    config = app['config'].dict()
    assert config == {'debug': True, 'database': {'host': 'some_host', 'port': 5555}}