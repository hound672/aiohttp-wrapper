from aiohttp import web
from aiohttp import hdrs
from aiohttp.web_response import StreamResponse


class ValidateView(web.View):
    """View class with validations"""

    async def _iter(self) -> StreamResponse:
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()

        method_name = self.request.method.lower()
        method = getattr(self, method_name, None)
        if method is None:
            self._raise_allowed_methods()

        body_schema_field = f'{method_name}_body'
        body_schema = getattr(self, body_schema_field, None)
        if body_schema is not None:
            try:
                body_data = await self.request.json()
            except Exception as e:
                return web.json_response({'error': 'error'})

        resp = await method()
        return resp
