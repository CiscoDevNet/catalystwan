import re
from functools import wraps
from pprint import pformat
from typing import Any, Callable, Dict, Optional, Sequence, Type, TypeVar, Union, cast
from urllib.parse import urlparse

from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel as BaseModelV1
from requests import PreparedRequest, Request, Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import JSONDecodeError

from vmngclient import with_proc_info_header
from vmngclient.endpoints import APIEndpointClientResponse
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass

T = TypeVar("T")
PRINTABLE_CONTENT = re.compile(r"(text\/.+)|(application\/(json|html|xhtml|xml|x-www-form-urlencoded))", re.IGNORECASE)
SENSITIVE_URL_PATHS = ["/dataservice/settings/configuration/smartaccountcredentials"]


class ErrorInfo(BaseModelV2):
    message: Union[str, None]
    details: Union[str, None]
    code: Union[str, None]


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
    if content_type := {k.lower(): v for k, v in _request.headers.items()}.get("content-type"):
        if not re.search(PRINTABLE_CONTENT, content_type):
            del request_debug["body"]
    if urlparse(_request.url).path in SENSITIVE_URL_PATHS:
        del request_debug["body"]
        del request_debug["json"]
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

            if isinstance(json, dict):
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


def parse_cookies_to_dict(cookies: str) -> Dict[str, str]:
    """Utility method to parse cookie string into dict"""
    result: Dict[str, str] = {}
    for item in cookies.split(";"):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            result[item] = ""
            continue
        name, value = item.split("=", 1)
        result[name] = value
    return result


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


class vManageResponse(Response, APIEndpointClientResponse):
    """Extends Response object with methods specific to vManage.
    Object is meant to be created from aready received requests.Response"""

    def __init__(self, response: Response):
        self.__dict__.update(response.__dict__)
        if not self.cookies.keys():
            self.cookies = self.__parse_set_cookie_from_headers()
        try:
            self.payload = JsonPayload(response.json())
        except JSONDecodeError:
            self.payload = JsonPayload()

    def __parse_set_cookie_from_headers(self) -> RequestsCookieJar:
        """Parses "set-cookie" content from response headers"""
        jar = RequestsCookieJar()
        cookies_string = self.headers.get("set-cookie", "")
        jar.update(parse_cookies_to_dict(cookies_string))
        return jar

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

    def dataseq(self, cls: Type[T], sourcekey: Optional[str] = "data") -> DataSequence[T]:
        """Returns data contents from JSON payload parsed as DataSequence of Dataclass/BaseModel instances
        Args:
            cls: Dataclass/BaseModelV1 subtype (eg. Devices)
            sourcekey: name of the JSON key from response payload to be parsed. If None whole JSON payload will be used

        Returns:
            DataSequence[T] of given type T which is subclassing from Dataclass/BaseModel,
            in case JSON payload was containing a single Object - sequence with one element is returned
        """
        if sourcekey is None:
            data = self.payload.json
        else:
            data = self.payload.json.get(sourcekey)

        if isinstance(data, Sequence):
            sequence = data
        else:
            sequence = [cast(dict, data)]

        if issubclass(cls, BaseModelV1):
            return DataSequence(cls, [cls.parse_obj(item) for item in sequence])  # type: ignore
        if issubclass(cls, BaseModelV2):
            return DataSequence(cls, [cls.model_validate(item) for item in sequence])  # type: ignore
        return DataSequence(cls, [create_dataclass(cls, item) for item in sequence])

    def dataobj(self, cls: Type[T], sourcekey: Optional[str] = "data") -> T:
        """Returns data contents from JSON payload parsed as Dataclass/BaseModel instance
        Args:
            cls: Dataclass/BaseModel subtype (eg. Devices)
            sourcekey: name of the JSON key from response payload to be parsed. If None whole JSON payload will be used

        Returns:
            Object of given type T which is subclassing from Dataclass/BaseModel,

        """
        if sourcekey is None:
            data = self.payload.json
        else:
            data = self.payload.json.get(sourcekey)

        if issubclass(cls, BaseModelV1):
            return cls.parse_obj(data)  # type: ignore
        if issubclass(cls, BaseModelV2):
            return cls.model_validate(data)  # type: ignore
        return create_dataclass(cls, data)

    def get_error_info(self) -> ErrorInfo:
        """Returns error information from JSON payload"""

        if self.payload.error is None:
            return ErrorInfo(
                message=None,
                details=None,
                code=None,
            )

        return ErrorInfo(**self.payload.error)


def with_vmanage_response(method: Callable[[Any], Response]) -> Callable[[Any], vManageResponse]:
    @wraps(method)
    def wrapper(*args, **kwargs) -> vManageResponse:
        return vManageResponse(method(*args, **kwargs))

    return wrapper
