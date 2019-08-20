from typing import Optional

class WrapperHttpException(Exception):
    _status_code: int
    _reason: str
    _details: Optional[dict]

    def __init__(self, details: Optional[dict] = None):
        self._details = details

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def details(self) -> Optional[dict]:
        return self._details


class HttpBadRequest(WrapperHttpException):
    _reason = 'ERR_BAD_REQUEST'
    _status_code = 400
