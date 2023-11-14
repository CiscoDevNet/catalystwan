# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import Any, List, Optional

from packaging.version import Version  # type: ignore
from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get


class VersionField(Version):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        return Version(value)


class ServerInfo(BaseModel):
    server: Optional[str]
    tenancy_mode: Optional[str] = Field(alias="tenancyMode")
    user_mode: Optional[str] = Field(alias="userMode")
    vsession_id: Optional[str] = Field(alias="VSessionId")
    is_saml_user: Optional[bool] = Field(alias="isSamlUser")
    is_rbac_vpn_user: Optional[bool] = Field(alias="isRbacVpnUser")
    vpns: List[Any] = []
    csrf_token: Optional[str] = Field(alias="CSRFToken")
    provider_domain: Optional[str] = Field(alias="providerDomain")
    tenant_id: Optional[str] = Field(alias="tenantId")
    provider_id: Optional[str] = Field(alias="providerId")
    view_mode: Optional[str] = Field(alias="viewMode")
    capabilities: List[str] = []
    user: Optional[str]
    description: Optional[str]
    locale: Optional[str]
    roles: List[str] = []
    external_user: Optional[bool] = Field(alias="externalUser")
    platform_version: str = Field(default="", alias="platformVersion")
    general_template: Optional[bool] = Field(alias="generalTemplate")
    disable_full_config_push: Optional[bool] = Field(alias="disableFullConfigPush")
    enable_server_events: Optional[bool] = Field(alias="enableServerEvents")
    cloudx: Optional[str]
    reverseproxy: Optional[str]
    vmanage_mode: Optional[str] = Field(alias="vmanageMode")


class AboutInfo(BaseModel):
    title: Optional[str]
    version: str = Field(default="")
    application_version: Optional[str] = Field(alias="applicationVersion")
    application_server: Optional[str] = Field(alias="applicationServer")
    copyright: Optional[str]
    time: Optional[datetime]
    time_zone: Optional[str] = Field(alias="timeZone")
    logo: Optional[str]


class ServerReady(BaseModel):
    is_server_ready: bool = Field(alias="isServerReady")


class Client(APIEndpoints):
    @get("/client/server", "data")
    def server(self) -> ServerInfo:
        ...

    @get("/client/server/ready")
    def server_ready(self) -> ServerReady:
        ...

    @get("/client/about", "data")
    def about(self) -> AboutInfo:
        ...
