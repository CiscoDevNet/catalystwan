# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, IPvAnyAddress

from vmngclient.endpoints import APIEndpoints, get, request
from vmngclient.typed_list import DataSequence


class Mode(str, Enum):
    on = "on"
    off = "off"


class Organization(BaseModel):
    domain_id: str = Field(alias="domain-id")
    org: str
    control_connection_up: bool = Field(alias="controlConnectionUp")


class Device(BaseModel):
    domain_ip: IPvAnyAddress = Field(alias="domainIp")
    port: int = Field(ge=1, le=65536)


class EmailNotificationSettings(BaseModel):
    enabled: bool


class HardwareRootCA(BaseModel):
    hardware_certificate: str = Field(alias="hardwareCertificate")
    control_connection_up: bool = Field(alias="controlConnectionUp")


class Certificate(BaseModel):
    certificate_signing: str = Field(alias="certificateSigning")
    validity_period: str = Field(alias="validityPeriod")
    retrieve_interval: str = Field(alias="retrieveInterval")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    email: Optional[str] = Field(default=None)


class VEdgeCloud(BaseModel):
    certificateauthority: str


class Banner(BaseModel):
    mode: Mode


class ProxyHTTPServer(BaseModel):
    proxy: bool
    proxy_ip: str = Field(default="", alias="proxyIp")
    proxy_port: str = Field(default="", alias="proxyPort")


class ReverseProxy(BaseModel):
    mode: Mode


class CloudX(BaseModel):
    mode: Mode


class ManageEncryptedPassword(BaseModel):
    manage_type8_password: bool = Field(alias="manageType8Password")


class ConfigurationSettings(APIEndpoints):
    def create_analytics_data_file(self):
        # POST /settings/configuration/analytics/dca
        ...

    def edit_cert_configuration(self):
        # PUT /settings/configuration/certificate/{settingType}
        ...

    def edit_configuration(self):
        # PUT /settings/configuration/{settingType}
        ...

    def get_banner(self):
        # GET /settings/banner
        ...

    def get_cert_configuration(self):
        # GET /settings/configuration/certificate/{settingType}
        ...

    @request(get, "/settings/configuration/{setting_type}")
    def get_configuration_by_setting_type(self, setting_type: str) -> dict:
        ...

    @request(get, "/settings/configuration/organization", "data")
    def get_organizations(self) -> DataSequence[Organization]:
        ...

    @request(get, "/settings/configuration/device", "data")
    def get_devices(self) -> DataSequence[Device]:
        ...

    @request(get, "/settings/configuration/emailNotificationSettings", "data")
    def get_email_notification_settings(self) -> DataSequence[EmailNotificationSettings]:
        ...

    @request(get, "/settings/configuration/hardwarerootca", "data")
    def get_hardware_root_cas(self) -> DataSequence[HardwareRootCA]:
        ...

    @request(get, "/settings/configuration/certificate", "data")
    def get_certificates(self) -> DataSequence[Certificate]:
        ...

    @request(get, "/settings/configuration/vedgecloud", "data")
    def get_vedge_cloud(self) -> DataSequence[VEdgeCloud]:
        ...

    @request(get, "/settings/configuration/banner", "data")
    def get_banners(self) -> DataSequence[Banner]:
        ...

    @request(get, "/settings/configuration/proxyHttpServer", "data")
    def get_proxy_http_servers(self) -> DataSequence[ProxyHTTPServer]:
        ...

    @request(get, "/settings/configuration/reverseproxy", "data")
    def get_reverse_proxies(self) -> DataSequence[ReverseProxy]:
        ...

    @request(get, "/settings/configuration/cloudx", "data")
    def get_cloudx(self) -> DataSequence[CloudX]:
        ...

    @request(get, "/settings/configuration/manageEncryptedPassword", "data")
    def get_manage_encrypted_password(self) -> DataSequence[ManageEncryptedPassword]:
        ...

    def get_google_map_key(self):
        # GET /settings/configuration/googleMapKey
        ...

    def get_maintenance_window(self):
        # GET /settings/configuration/maintenanceWindow
        ...

    def get_password_policy(self):
        # GET /settings/passwordPolicy
        ...

    def get_session_timout(self):
        # GET /settings/clientSessionTimeout
        ...

    def new_cert_configuration(self):
        # POST /settings/configuration/certificate/{settingType}
        ...

    def new_configuration(self):
        # POST /settings/configuration/{settingType}
        ...
