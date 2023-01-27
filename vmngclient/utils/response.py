from pprint import pformat
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

from requests import PreparedRequest, Request, Response
from requests.exceptions import JSONDecodeError

from vmngclient.utils.creation_tools import create_dataclass

T = TypeVar("T")


class VManageResponseException(Exception):
    def __init__(self, message: str, response: Response):
        self.message = message
        self.response = response

    def __str__(self):
        return f"{self.message}\n{response_debug(self.response)}"


def response_debug(response: Optional[Response], request: Union[Request, PreparedRequest, None]) -> str:
    """Returns human readable string containing Request-Response contents (helpful for debugging).

    Args:
        response: Response object to be debugged (note it contains an PreparedRequest object already)
        request: optional Request object to be debugged

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

    Returns:
        str
    """
    if response is None:
        return response_debug(response, request)
    response_debugs = [response_debug(resp, None) for resp in response.history]
    response_debugs += [response_debug(response, request)]
    return "\n".join(response_debugs)


def get_json_data(response: Response) -> Any:
    try:
        response_json = response.json()
    except JSONDecodeError:
        raise VManageResponseException("Response does not contain a valid json", response)
    if isinstance(response_json, dict) and "data" in response_json.keys():
        return response_json.get("data")
    else:
        raise VManageResponseException("{'data': ... } field not found in Response", response)


def get_json_data_as_list(response: Response) -> List:
    data = get_json_data(response)
    if not isinstance(data, list):
        raise VManageResponseException(f"{{'data'\"': ...}} contains {type(data)}, expected list", response)
    return cast(list, data)


def get_json_data_as_dict(response: Response) -> Dict[str, Any]:
    data = get_json_data(response)
    if not isinstance(data, Dict):
        raise VManageResponseException(f"{{'data': ...}} contains {type(data)}, expected dict", response)
    return cast(dict, data)


def parse_as(response: Response, cls: Type[T]) -> T:
    try:
        return create_dataclass(cls, get_json_data_as_dict(response))
    except TypeError as e:
        raise VManageResponseException(f"Cannot create {cls}: {str(e)}", response)


def parse_as_list(response: Response, cls: Type[T]) -> List[T]:
    try:
        items = get_json_data_as_list(response)
        return [create_dataclass(cls, item) for item in items]
    except TypeError as e:
        raise VManageResponseException(f"Cannot create {cls}: {str(e)}", response)
