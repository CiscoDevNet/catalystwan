# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Optional, Protocol, Type, TypeVar

from packaging.version import Version  # type: ignore

from catalystwan.typed_list import DataSequence
from catalystwan.utils.session_type import SessionType

T = TypeVar("T")


class APIEndpointClientResponse(Protocol):
    """
    Interface to response object. Fits "requests.Response"
    but set of methods is minimal to allow easy migration to another client if needed
    """

    @property
    def text(self) -> str:
        ...

    @property
    def content(self) -> bytes:
        ...

    def dataobj(self, cls: Type[T], sourcekey: Optional[str]) -> T:
        ...

    def dataseq(self, cls: Type[T], sourcekey: Optional[str]) -> DataSequence[T]:
        ...

    def json(self) -> dict:
        ...


class APIEndpointClient(Protocol):
    """
    Interface to client object.
    We only need a 'request' function and few vmanage session properties obtained from server.
    Matched to fit "requests.Session" but migration to other client is possible.
    At his point not very clean as injection of custom kwargs is possible (and sometimes used)
    """

    def request(self, method: str, url: str, **kwargs) -> APIEndpointClientResponse:
        ...

    @property
    def api_version(self) -> Optional[Version]:
        ...

    @property
    def session_type(self) -> Optional[SessionType]:
        ...
