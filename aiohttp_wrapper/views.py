from aiohttp import web
from aiohttp import hdrs
from aiohttp.web_response import StreamResponse
from pydantic import ValidationError


from aiohttp_wrapper import exceptions as wrapper_exceptions

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
                raise wrapper_exceptions.HttpBadRequest(reason='ERR_NO_JSON')

            try:
                body_values = body_schema(**body_data)
            except ValidationError as e:
                raise wrapper_exceptions.HttpBadRequest(
                    reason='ERR_VALIDATION',
                    details=e.errors()
                )

        resp = await method()
        return resp
