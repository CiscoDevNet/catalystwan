from functools import wraps
from pprint import pformat
from typing import Any, Callable, Optional, Sequence, Type, TypeVar, Union, cast

from attr import define  # type: ignore
from requests import PreparedRequest, Request, Response
from requests.exceptions import JSONDecodeError

from vmngclient import with_proc_info_header
from vmngclient.dataclasses import DataclassBase
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass

T = TypeVar("T")


@define(frozen=True)
class ErrorInfo(DataclassBase):
    message: str
    details: str
    code: str


def response_debug(response: Optional[Response], request: Union[Request, PreparedRequest, None]) -> str:
    """Returns human readable string containing Request-Response contents (helpful for debugging).

    Args:
        response: Response object to be debugged (note it contains an PreparedRequest object already)
        request: optional Request object to be debugged

    When response is provided, request argument is ignored and contents of reqest.response will be returned.

    Returns:
        str
    """
    if request is None:
        if response is None:
            return ""
        else:
            _request: Union[Request, PreparedRequest] = response.request
    else:
        _request = request
    debug_dict = {}
    request_debug = {
        "method": _request.method,
        "url": _request.url,
        "headers": dict(_request.headers.items()),
        "body": getattr(_request, "body", None),
        "json": getattr(_request, "json", None),
    }
    debug_dict["request"] = {k: v for k, v in request_debug.items() if v is not None}
    if response is not None:
        response_debug = {
            "status": response.status_code,
            "reason": response.reason,
            "elapsed-seconds": round(float(response.elapsed.microseconds) / 1000000, 3),
            "headers": dict(response.headers.items()),
        }
        try:
            json = response.json()
            json.pop("header", None)
            response_debug.update({"json": json})
        except JSONDecodeError:
            if response.encoding is not None:
                if len(response.text) <= 1024:
                    response_debug.update({"text": response.text})
                else:
                    response_debug.update({"text(trimmed)": response.text[:1024]})
            else:
                response_debug.update({"text(cannot convert to string: unknown encoding)": None})
        debug_dict["response"] = response_debug
    return pformat(debug_dict, width=80, sort_dicts=False)


@with_proc_info_header
def response_history_debug(response: Optional[Response], request: Union[Request, PreparedRequest, None]) -> str:
    """Returns human readable string containing Request-Response history contents for given response.

    Args:
        response: Response object to be debugged (note it contains an PreparedRequest object already)
        request: optional Request object to be debugged (considered to be latest request)

    When response is provided, request argument is ignored and contents of reqest.response will be returned.

    Returns:
        str
    """
    if response is None:
        return response_debug(response, request)
    response_debugs = [response_debug(resp, None) for resp in response.history]
    response_debugs += [response_debug(response, request)]
    return "\n".join(response_debugs)


class JsonPayload:
    def __init__(self, json: Any = None):
        self.json = json
        self.data = None
        self.error = None
        self.headers = None
        if isinstance(json, dict):
            self.data = json.get("data", None)
            self.error = json.get("error", None)
            self.headers = json.get("headers", None)


class vManageResponse(Response):
    """Extends Response object with methods specific to vManage"""

    def __init__(self, response: Response):
        self.__dict__.update(response.__dict__)
        try:
            self.payload = JsonPayload(response.json())
        except JSONDecodeError:
            self.payload = JsonPayload()

    def info(self, history: bool = False) -> str:
        """Returns human readable string containing Request-Response contents
        Args:
            history: include response history (eg. redirects)

        Returns:
            str
        """
        if history:
            return response_history_debug(self, None)
        return response_debug(self, None)

    def dataseq(self, cls: Type[T]) -> DataSequence[T]:
        """Returns data contents from JSON payload deserialized to Sequence of Dataclass instances
        Args:
            cls: Dataclass subtype (eg. Devices)

        Returns:
            DataSequence of given type,
            in case JSON payload was containing a single Object - sequence with one element is returned
        """
        data = self.payload.data
        if isinstance(data, Sequence):
            sequence = data
        else:
            sequence = [cast(dict, data)]
        return DataSequence(cls, [create_dataclass(cls, item) for item in sequence])

    def get_error_info(self) -> ErrorInfo:
        """Returns error information from JSON payload"""
        return create_dataclass(ErrorInfo, cast(dict, self.payload.error))


def with_vmanage_response(method: Callable[[Any], Response]) -> Callable[[Any], vManageResponse]:
    @wraps(method)
    def wrapper(*args, **kwargs) -> vManageResponse:
        return vManageResponse(method(*args, **kwargs))

    return wrapper
