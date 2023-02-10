from functools import wraps
from pprint import pformat
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

from requests import PreparedRequest, Request, Response
from requests.exceptions import JSONDecodeError

from vmngclient.dataclasses import vManageResponseErrorData
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass

T = TypeVar("T")


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
            "headers": dict(response.headers.items()),
        }
        try:
            json = response.json()
            json.pop("header", None)
            response_debug.update({"json": json})
        except JSONDecodeError:
            if len(response.text) <= 1024:
                response_debug.update({"text": response.text})
            else:
                response_debug.update({"text(trimmed)": response.text[:128]})
        debug_dict["response"] = response_debug
    return pformat(debug_dict, width=80, sort_dicts=False)


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
    """Extension of Response with methods specific to vManage"""

    def __init__(self, response: Response):
        self.__dict__.update(response.__dict__)
        try:
            self.payload = JsonPayload(response.json())
        except JSONDecodeError:
            self.payload = JsonPayload()

    def info(self, history: bool = False) -> str:
        """Returns human readable string containing Request-Response contents"""
        if history:
            return response_history_debug(self, None)
        return response_debug(self, None)

    def parse(self, cls: Type[T]) -> T:
        try:
            return create_dataclass(cls, self.__get_json_data_as_dict())
        except TypeError as e:
            raise vManageResponseException(f"Cannot parse {cls}: {str(e)}", self)

    def parse_list(self, cls: Type[T]) -> DataSequence[T]:
        try:
            items = self.__get_json_data_as_list()
            return DataSequence(cls, [create_dataclass(cls, item) for item in items])
        except TypeError as e:
            raise vManageResponseException(f"Cannot parse {cls}: {str(e)}", self)

    def get_error(self) -> vManageResponseErrorData:
        try:
            return create_dataclass(vManageResponseErrorData, self.__get_error_dict())
        except TypeError as e:
            raise vManageResponseException(f"Cannot parse {vManageResponseErrorData}: {str(e)}", self)

    def __get_json_data_as_list(self) -> List:
        data = self.payload.data
        if not isinstance(data, list):
            raise vManageResponseException(f"{{'data'\"': ...}} contains {type(data)}, expected list", self)
        return cast(list, data)

    def __get_json_data_as_dict(self) -> Dict[str, Any]:
        data = self.payload.data
        if not isinstance(data, Dict):
            raise vManageResponseException(f"{{'data': ...}} contains {type(data)}, expected dict", self)
        return cast(dict, data)

    def __get_error_dict(self) -> Dict[str, str]:
        error = self.payload.error
        if not isinstance(error, Dict):
            raise vManageResponseException(f"{{'error': ...}} contains {type(error)}, expected dict", self)
        return cast(dict, error)


def with_vmanage_response(method: Callable[[Any], Response]) -> Callable[[Any], vManageResponse]:
    @wraps(method)
    def wrapper(*args, **kwargs) -> vManageResponse:
        return vManageResponse(method(*args, **kwargs))

    return wrapper


class vManageResponseException(Exception):
    def __init__(self, message: str, response: vManageResponse):
        self.message = message
        self.response = response

    def __str__(self):
        return f"{self.message}\n{self.response}"
