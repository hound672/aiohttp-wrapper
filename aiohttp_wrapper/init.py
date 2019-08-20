from aiohttp import web

from .middlewares import middleware_error

async def init_aiohttp_wrapper(app: web.Application) -> None:
    """
    Init aiohttp wrapper
    """

    app.middlewares.append(middleware_error)
