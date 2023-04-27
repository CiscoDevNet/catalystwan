from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Final, Iterable, Mapping, Optional, Sequence, Set, TypedDict, Union

from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import BaseModel

from vmngclient.exceptions import APIRequestPayloadTypeError, APIVersionError, APIViewError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import AttrsInstance, asdict

if TYPE_CHECKING:
    from vmngclient.response import vManageResponse
    from vmngclient.session import SessionType, vManageSession


BASE_PATH: Final[str] = "/dataservice"
logger = logging.getLogger(__name__)
PayloadType = Union[DataSequence, Sequence[Union[AttrsInstance, BaseModel]], AttrsInstance, BaseModel]


class PreparedPayload(TypedDict):
    data: Union[str, bytes]
    headers: Mapping[str, str]


def prepare_payload(payload: PayloadType) -> PreparedPayload:
    if isinstance(payload, BaseModel):
        return _prepare_basemodel_payload(payload)
    if isinstance(payload, AttrsInstance):
        return _prepare_attrs_payload(payload)
    if isinstance(payload, (DataSequence, Sequence)):
        return _prepare_sequence_payload(payload)
    else:
        raise APIRequestPayloadTypeError(payload)


def _prepare_basemodel_payload(payload: BaseModel) -> PreparedPayload:
    return PreparedPayload(
        data=payload.json(exclude_none=True, by_alias=True), headers={"content-type": "application/json"}
    )


def _prepare_attrs_payload(payload: AttrsInstance) -> PreparedPayload:
    return PreparedPayload(data=json.dumps(asdict(payload)), headers={"content-type": "application/json"})


def _prepare_sequence_payload(payload: Iterable[Union[BaseModel, AttrsInstance]]) -> PreparedPayload:
    items = []
    for item in payload:
        if isinstance(item, BaseModel):
            items.append(item.dict(exclude_none=True, by_alias=True))
        elif isinstance(item, AttrsInstance):
            items.append(asdict(item))
        else:
            raise APIRequestPayloadTypeError(payload)
    data = json.dumps(items)
    return PreparedPayload(data=data, headers={"content-type": "application/json"})


class APIPrimitiveBase:
    def __init__(self, session: vManageSession):
        self.session = session
        self.basepath = BASE_PATH

    def request(self, method: str, url: str, payload: Optional[PayloadType] = None, **kwargs) -> vManageResponse:
        if payload is not None:
            kwargs.update(prepare_payload(payload))
        return self.session.request(method, self.basepath + url, **kwargs)

    def get(self, url: str, payload: Optional[PayloadType] = None, **kwargs) -> vManageResponse:
        return self.request("GET", url, payload, **kwargs)

    def put(self, url: str, payload: Optional[PayloadType] = None, **kwargs) -> vManageResponse:
        return self.request("PUT", url, payload, **kwargs)

    def post(self, url: str, payload: Optional[PayloadType] = None, **kwargs) -> vManageResponse:
        return self.request("POST", url, payload, **kwargs)

    def delete(self, url: str, payload: Optional[PayloadType] = None, **kwargs) -> vManageResponse:
        return self.request("DELETE", url, payload, **kwargs)

    @property
    def version(self) -> Optional[Version]:
        return self.session.api_version

    @property
    def session_type(self) -> Optional[SessionType]:
        return self.session.session_type


class Versions:
    """
    Decorator to annotate api primitives methods with supported versions.
    Logs warning or raises exception when incompatibility found.
    """

    def __init__(self, supported_versions: str, raises: bool = False):
        self.supported_versions = SpecifierSet(supported_versions)
        self.raises = raises

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise TypeError("Only APIPrimitiveBase instance methods can be annotated with @Versions decorator")
            current = api.version
            supported = self.supported_versions
            if current and current not in supported:
                if self.raises:
                    raise APIVersionError(func, supported, current)
                else:
                    logger.warning(
                        f"vManage runs: {current} but {func.__qualname__} only supported for API versions: {supported}"
                    )
            return func(*args, **kwargs)

        return wrapper


class View:
    """
    Decorator to annotate api primitives methods with session type (view) restriction
    Logs warning or raises exception when incompatibility found.
    """

    def __init__(self, allowed_session_types: Set[SessionType], raises: bool = False):
        self.allowed_session_types = allowed_session_types
        self.raises = raises

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise TypeError("Only APIPrimitiveBase instance methods can be annotated with @Versions decorator")
            current = api.session_type
            allowed = self.allowed_session_types
            if current and current not in allowed:
                if self.raises:
                    raise APIViewError(func, allowed, current)
                else:
                    logger.warning(
                        f"Current view is: {current} but {func.__qualname__} only allowed for views: {allowed}"
                    )
            return func(*args, **kwargs)

        return wrapper
