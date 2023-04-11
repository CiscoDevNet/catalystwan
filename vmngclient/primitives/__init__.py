from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore

from vmngclient.exceptions import APIVersionException

if TYPE_CHECKING:
    from vmngclient.response import vManageResponse
    from vmngclient.session import vManageSession


BasePath = "/dataservice"
logger = logging.getLogger(__name__)


class APIPrimitiveBase:
    def __init__(self, session: vManageSession):
        self.session = session
        self.basepath = BasePath

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


class Versions:
    """
    decorator to annotate api primitives methods with supported versions
    logs warning or raises exception when incompatibility found
    """

    def __init__(self, versions: str, raises: bool = False):
        self.versions = SpecifierSet(versions)
        self.raises = raises

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise TypeError("Only APIPrimitiveBase instance methods can be annotated with @Versions decorator")
            current = api.session.api_version
            supported = self.versions
            if current and current not in supported:
                if self.raises:
                    raise APIVersionException(func, supported, current)
                else:
                    logger.warning(
                        f"vManage runs: {current} but {func.__qualname__} only supported for API versions: {supported}"
                    )
            return func(*args, **kwargs)

        return wrapper


class VersionField(Version):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        return Version(value)
