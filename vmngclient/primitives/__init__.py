from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Final, Optional, Set

from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore

from vmngclient.exceptions import APIVersionError, APIViewError

if TYPE_CHECKING:
    from vmngclient.response import vManageResponse
    from vmngclient.session import SessionType, vManageSession


BASE_PATH: Final[str] = "/dataservice"
logger = logging.getLogger(__name__)


class APIPrimitiveBase:
    def __init__(self, session: vManageSession):
        self.session = session
        self.basepath = BASE_PATH

    def request(self, method: str, urn: str, *args, **kwargs) -> vManageResponse:
        return self.session.request(method, self.basepath + urn, *args, **kwargs)

    def get(self, urn: str, *args, **kwargs) -> vManageResponse:
        return self.request("GET", urn, *args, **kwargs)

    def put(self, urn: str, *args, **kwargs) -> vManageResponse:
        return self.request("PUT", urn, *args, **kwargs)

    def post(self, urn: str, *args, **kwargs) -> vManageResponse:
        return self.request("POST", urn, *args, **kwargs)

    def delete(self, urn: str, *args, **kwargs) -> vManageResponse:
        return self.request("DELETE", urn, *args, **kwargs)

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
