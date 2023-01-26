from dataclasses import dataclass
from pprint import pformat
from typing import Any, Dict, List, Type, TypeVar, Union, cast

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


@dataclass
class VManageResponseDebugInfo:
    request: Dict[str, Any]
    response: Dict[str, Any]


def response_debug(response: Response, request: Union[Request, PreparedRequest, None]) -> str:
    """Returns human readable string containing Request-Response contents (helpful for debugging).

    Args:
        response: Response object to be debugged (note it contains an PreparedRequest object already)
        request: optional Request object to be debugged

    Returns:
        str
    """
    if request is None:
        request = response.request
        request_body = request.body
    else:
        request = request
        request_body = None
    info = VManageResponseDebugInfo(
        request={
            "method": request.method,
            "url": request.url,
            "body": request_body,
            "headers": dict(request.headers.items()),
        },
        response={
            "status": response.status_code,
            "reason": response.reason,
            "headers": dict(response.headers.items()),
        },
    )
    try:
        json = response.json()
        json.pop("header", None)
        info.response.update({"json": json})
    except JSONDecodeError:
        if len(response.text) <= 1024:
            info.response.update({"text": response.text})
        else:
            info.response.update({"text(trimmed)": response.text[:128]})
    return pformat(dict(info.__dict__.items()), width=80, sort_dicts=False)


def response_history_debug(response: Response, request: Union[Request, PreparedRequest, None]) -> str:
    """Returns human readable string containing Request-Response history contents for given response.

    Args:
        response: Response object to be debugged (note it contains an PreparedRequest object already)
        request: optional Request object to be debugged (considered to be latest request)

    Returns:
        str
    """
    response_debugs = [response_debug(resp, None) for resp in response.history] + [response_debug(response, request)]
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
