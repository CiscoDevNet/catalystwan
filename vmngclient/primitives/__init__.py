from __future__ import annotations

import json
import logging
from inspect import Signature, _empty, isclass, signature
from string import Formatter

# from pydoc import locate
from typing import (
    Any,
    BinaryIO,
    Final,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    TypedDict,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from attr import dataclass
from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import BaseModel

from vmngclient.dataclasses import DataclassBase
from vmngclient.exceptions import APIPrimitiveError, APIVersionError, APIViewError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import AttrsInstance, asdict
from vmngclient.utils.session_type import SessionType

BASE_PATH: Final[str] = "/dataservice"
T = TypeVar("T")
logger = logging.getLogger(__name__)
ModelPayloadType = Union[AttrsInstance, BaseModel, Sequence[AttrsInstance], Sequence[BaseModel]]
PayloadType = Union[None, str, bytes, dict, BinaryIO, ModelPayloadType]


@dataclass(kw_only=True)
class EndpointMeta:
    http_method: str
    url: str
    versions: Optional[SpecifierSet] = None
    tenancy_mode: Optional[Set[SessionType]] = None
    primitive_class: type
    primitive_method: Any
    payload_type: type
    payload_collection_type: Optional[type]
    return_type: type
    return_collection_type: Optional[type]


class EndpointMetaRegistry:
    def __init__(self):
        self.items: dict[Any, EndpointMeta] = {}
        self.versions_cache: dict[Any, SpecifierSet] = {}
        self.tenancy_mode_cache: dict[Any, Set[SessionType]] = {}

    def register(self, func, meta: EndpointMeta):
        if self.items.get(func):
            raise APIPrimitiveError(f"{func} already registered")
        # if version, tenancy annotations was added before required data
        meta.versions = self.versions_cache.pop(func, None)
        meta.tenancy_mode = self.tenancy_mode_cache.pop(func, None)
        self.items[func] = meta

    def update_versions(self, func, versions: SpecifierSet):
        if item := self.items.get(func):
            item.versions = versions
        else:
            self.versions_cache[func] = versions

    def update_tenacy_mode(self, func, tenancy_mode: Set[SessionType]):
        if item := self.items.get(func):
            item.tenancy_mode = tenancy_mode
        else:
            self.tenancy_mode_cache[func] = tenancy_mode


class PreparedPayload(TypedDict):
    data: Union[str, bytes]
    headers: Mapping[str, str]


def prepare_payload(payload: ModelPayloadType) -> PreparedPayload:
    if isinstance(payload, BaseModel):
        return _prepare_basemodel_payload(payload)
    if isinstance(payload, AttrsInstance):
        return _prepare_attrs_payload(payload)
    if isinstance(payload, (DataSequence, Sequence)):
        return _prepare_sequence_payload(payload)
    else:
        raise APIPrimitiveError(payload)


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
            raise APIPrimitiveError(payload)
    data = json.dumps(items)
    return PreparedPayload(data=data, headers={"content-type": "application/json"})


class APIPRimitiveClientResponse(Protocol):
    @property
    def text(self) -> str:
        ...

    @property
    def content(self) -> bytes:
        ...

    def dataobj(self, cls: Type[T], sourcekey: Optional[str] = "data") -> T:
        ...

    def dataseq(self, cls: Type[T], sourcekey: Optional[str] = "data") -> DataSequence[T]:
        ...

    def json(self) -> dict:
        ...


class APIPrimitiveClient(Protocol):
    def request(self, method: str, url: str, **kwargs) -> APIPRimitiveClientResponse:
        ...

    @property
    def api_version(self) -> Optional[Version]:
        ...

    @property
    def session_type(self) -> Optional[SessionType]:
        ...


class APIPrimitiveBase:
    def __init__(self, client: APIPrimitiveClient):
        self._client = client
        self._basepath = BASE_PATH

    def _request(
        self, method: str, url: str, payload: Optional[ModelPayloadType] = None, **kwargs
    ) -> APIPRimitiveClientResponse:
        if payload is not None:
            kwargs.update(prepare_payload(payload))
        return self._client.request(method, self._basepath + url, **kwargs)

    def _get(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("GET", url, payload, **kwargs)

    def _put(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("PUT", url, payload, **kwargs)

    def _post(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("POST", url, payload, **kwargs)

    def _delete(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("DELETE", url, payload, **kwargs)

    @property
    def _api_version(self) -> Optional[Version]:
        return self._client.api_version

    @property
    def _session_type(self) -> Optional[SessionType]:
        return self._client.session_type


endpoints = EndpointMetaRegistry()


class VersionsDecorator:
    """
    Decorator to annotate api primitives methods with supported versions.
    Logs warning or raises exception when incompatibility found.
    """

    def __init__(self, supported_versions: str, raises: bool = False):
        self.supported_versions = SpecifierSet(supported_versions)
        self.raises = raises

    def __call__(self, func):
        endpoints.update_versions(func, self.supported_versions)

        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise APIPrimitiveError(
                    "Only APIPrimitiveBase instance methods can be annotated with @versions decorator"
                )
            current = api._api_version
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


class ViewDecorator:
    """
    Decorator to annotate api primitives methods with session type (view) restriction
    Logs warning or raises exception when incompatibility found.
    """

    def __init__(self, allowed_session_types: Set[SessionType], raises: bool = False):
        self.allowed_session_types = allowed_session_types
        self.raises = raises

    def __call__(self, func):
        endpoints.update_tenacy_mode(func, self.allowed_session_types)

        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise APIPrimitiveError("Only APIPrimitiveBase instance methods can be annotated with @view decorator")
            current = api._session_type
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


class RequestDecorator:
    def __init__(self, method: str, url: str, resp_json_key: Optional[str] = None, **kwargs):
        self.method = method
        self.url = url
        self.resp_json_key = resp_json_key
        self.allowed_return_type = Union[
            bytes, str, dict, BinaryIO, BaseModel, DataclassBase, DataSequence[BaseModel], DataSequence[DataclassBase]
        ]

    def specify_return_type(self, sig: Signature) -> Tuple[bool, bool, type]:
        """Specifies return type to be used when parsing a reponse based on method signature annotations

        Args:
            sig (Signature): wrapped method signature

        Raises:
            APIPrimitiveError: when signature contains unexpected return annotation

        Returns:
            Tuple[bool, bool, type]: Specification (returns anyting?, is datasequence?, return type)
        """
        annotation = sig.return_annotation
        if isclass(annotation):
            if issubclass(annotation, (bytes, str, dict, BinaryIO, BaseModel, DataclassBase)):
                return (True, False, annotation)
            elif annotation == _empty:
                return (False, False, annotation)
            raise APIPrimitiveError(f"Expected: {self.allowed_return_type} but return type {annotation}")
        elif (type_origin := get_origin(annotation)) and isclass(type_origin) and issubclass(type_origin, DataSequence):
            if (
                (type_args := get_args(annotation))
                and (len(type_args) == 1)
                and isclass(type_args[0])
                and issubclass(type_args[0], (BaseModel, DataclassBase))
            ):
                return (True, True, type_args[0])
            raise APIPrimitiveError(f"Expected: {self.allowed_return_type} but return type {annotation}")
        else:
            raise APIPrimitiveError(f"Expected: {self.allowed_return_type} but return type {annotation}")

    def format_url(self, **kwargs) -> dict[str, Any]:
        """Formats url from keyword argumets given wrapped function

        Returns:
            dict[str, Any]: keyword arguments without fields consumed during parsing
        """
        formatter = Formatter()
        field_names = {item[1] for item in formatter.parse(self.url) if item[1] is not None}
        fields = {key: kwargs[key] for key in field_names}
        self.url.format(**fields)
        return {key: kwargs[key] for key in kwargs.keys() if key not in field_names}

    def __call__(self, func):
        self.returns, self.returns_dataseq, self.return_type = self.specify_return_type(signature(func))
        endpoints.register(
            func,
            EndpointMeta(
                http_method=self.method,
                url=self.url,
                primitive_class=func.__class__,
                primitive_method=func,
                payload_type=None,  # TODO
                payload_collection_type=None,  # TODO
                return_type=self.return_type,
                return_collection_type=DataSequence if self.returns_dataseq else None,
            ),
        )

        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise APIPrimitiveError(
                    "Only APIPrimitiveBase instance methods can be annotated with @request decorator"
                )
            request_kwargs = self.format_url(**kwargs)
            if self.returns:
                if issubclass(self.return_type, (BaseModel, DataclassBase)):
                    if self.returns_dataseq:
                        return api._request(self.method, self.url, **request_kwargs).dataseq(
                            self.return_type, self.resp_json_key
                        )
                    else:
                        return api._request(self.method, self.url, **request_kwargs).dataobj(
                            self.return_type, self.resp_json_key
                        )
                elif issubclass(self.return_type, str):
                    return api._request(self.method, self.url, **request_kwargs).text
                elif issubclass(self.return_type, bytes):
                    return api._request(self.method, self.url, **request_kwargs).content
                elif issubclass(self.return_type, dict):
                    return api._request(self.method, self.url, **request_kwargs).json()
            else:
                api._request(self.method, self.url, **request_kwargs)

        return wrapper


versions = VersionsDecorator
view = ViewDecorator
request = RequestDecorator
get = "GET"
post = "POST"
put = "PUT"
delete = "DELETE"
