from typing import Optional, Union, List, Dict

class WrapperHttpException(Exception):
    _status_code: int
    _reason: str
    _details: Union[Dict, List, None]

    def __init__(self,
                 reason: Optional[str] = None,
                 details: Union[Dict, List, None] = None):
        self._details = details
        if reason is not None:
            self._reason = reason

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def details(self) -> Union[Dict, List, None]:
        return self._details


class HttpBadRequest(WrapperHttpException):
    _reason = 'ERR_BAD_REQUEST'
    _status_code = 400
