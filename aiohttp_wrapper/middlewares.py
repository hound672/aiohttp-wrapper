from typing import Dict, Optional, Any, Union, List

from aiohttp import web, web_exceptions

from aiohttp_wrapper.exceptions import WrapperHttpException

@web.middleware
async def middleware_error(request: web.Request, handler: Any) -> web.Response:
    """
    Catch Http errors
    :param request:
    :param handler:
    :return:
    """

    def _error_http_response(status: int,
                             reason: Optional[str] = None,
                             details: Union[Dict, List, None] = None) -> web.Response:
        """
        Return aiohttp response with error and pass payload/reason into it.

        :param status: Error status code
        :param reason: error's reason
        :param errors: description of error/errors
        :return None
        """
        text_dict: Dict[str, Union[str, Dict, List]] = {}

        if reason is not None:
            text_dict['reason'] = reason

        if details is not None:
            text_dict['details'] = details

        return web.json_response(text_dict,
                                 status=status)

    def _make_error_reason_string(error_text: str) -> str:
        """
        Convert aiohttp error string to app format error string
        :param error_text: aiohttp error string
        :return: app format error string
        """
        return f'ERR_{error_text.upper().replace(" ", "_")}'

    try:
        response = await handler(request)

    except WrapperHttpException as e:
        return _error_http_response(
            status=e.status_code,
            reason=e.reason,
            details=e.details
        )

    except web_exceptions.HTTPClientError as e:  # catch aiohttp errors
        return _error_http_response(
            status=e.status_code,
            reason=_make_error_reason_string(e.reason)
        )

    except Exception as e:
        return _error_http_response(
            status=500,
            reason='ERR_INTERNAL_SERVER_ERROR'
        )

    else:
        return response
