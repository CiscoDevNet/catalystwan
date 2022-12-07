import json
from dataclasses import dataclass
from typing import Any, Dict, List, cast

from requests import Response
from requests.exceptions import JSONDecodeError


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


def response_debug(response: Response, headers: bool = False) -> str:
    request_body = response.request.body
    if isinstance(request_body, bytes):
        request_body = str(request_body, encoding="utf-8")
    info = VManageResponseDebugInfo(
        request={"method": response.request.method, "url": response.request.url, "body": request_body},
        response={"status": response.status_code, "reason": response.reason, "text": response.text},
    )
    if headers:
        info.request.update({"headers": dict(response.request.headers.items())})
        info.response.update({"headers": dict(response.headers.items())})
    return json.dumps(dict(info.__dict__.items()), indent=4)


def get_json_data(response: Response) -> Any:
    try:
        response_json = response.json()
    except JSONDecodeError:
        raise VManageResponseException("Response does not contain a valid json", response)
    if isinstance(response_json, dict) and "data" in response_json.keys():
        return response_json.get("data")
    else:
        raise VManageResponseException("{\"data\": ... } field not found in Response", response)


def get_json_data_as_list(response: Response) -> List:
    data = get_json_data(response)
    if not isinstance(data, list):
        raise VManageResponseException(f"{{\"data\": ...}} contains {type(data)}, expected list", response)
    return cast(list, data)


def get_json_data_as_dict(response: Response) -> Dict:
    data = get_json_data(response)
    if not isinstance(data, Dict):
        raise VManageResponseException(f"{{\"data\": ...}} contains {type(data)}, expected dict", response)
    return cast(dict, data)
