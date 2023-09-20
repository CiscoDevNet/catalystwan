# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import Any, List, Optional

from packaging.version import Version  # type: ignore
from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get


class VersionField(Version):
    @classmethod
    # TODO[pydantic]: Verify if that is working
    # Check https://docs.pydantic.dev/latest/migration/#defining-custom-types
    def __get_pydantic_core_schema__(cls) -> Version:
        return cls.validate

    @classmethod
    def validate(cls, value):
        return Version(value)


class ServerInfo(BaseModel):
    server: Optional[str] = None
    tenancy_mode: Optional[str] = Field(None, alias="tenancyMode")
    user_mode: Optional[str] = Field(None, alias="userMode")
    vsession_id: Optional[str] = Field(None, alias="VSessionId")
    is_saml_user: Optional[bool] = Field(None, alias="isSamlUser")
    is_rbac_vpn_user: Optional[bool] = Field(None, alias="isRbacVpnUser")
    vpns: List[Any] = []
    csrf_token: Optional[str] = Field(None, alias="CSRFToken")
    provider_domain: Optional[str] = Field(None, alias="providerDomain")
    tenant_id: Optional[str] = Field(None, alias="tenantId")
    provider_id: Optional[str] = Field(None, alias="providerId")
    view_mode: Optional[str] = Field(None, alias="viewMode")
    capabilities: List[str] = []
    user: Optional[str] = None
    description: Optional[str] = None
    locale: Optional[str] = None
    roles: List[str] = []
    external_user: Optional[bool] = Field(None, alias="externalUser")
    platform_version: str = Field(default="", alias="platformVersion")
    general_template: Optional[bool] = Field(None, alias="generalTemplate")
    disable_full_config_push: Optional[bool] = Field(None, alias="disableFullConfigPush")
    enable_server_events: Optional[bool] = Field(None, alias="enableServerEvents")
    cloudx: Optional[str] = None
    reverseproxy: Optional[str] = None
    vmanage_mode: Optional[str] = Field(None, alias="vmanageMode")


class AboutInfo(BaseModel):
    title: Optional[str] = None
    version: str = Field(default="")
    application_version: Optional[str] = Field(None, alias="applicationVersion")
    application_server: Optional[str] = Field(None, alias="applicationServer")
    copyright: Optional[str] = None
    time: Optional[datetime] = None
    time_zone: Optional[str] = Field(None, alias="timeZone")
    logo: Optional[str] = None


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
