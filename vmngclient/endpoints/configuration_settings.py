# mypy: disable-error-code="empty-body"
import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, IPvAnyAddress

from vmngclient.endpoints import APIEndpoints, get, request
from vmngclient.typed_list import DataSequence


class ModeEnum(str, Enum):
    on = "on"
    off = "off"


class DataStreamIPTypeEnum(str, Enum):
    system = "systemIp"
    mgmt = "mgmtIp"
    transport = "transportIp"


class Organization(BaseModel):
    domain_id: str = Field(alias="domain-id")
    org: str
    control_connection_up: bool = Field(alias="controlConnectionUp")


class Device(BaseModel):
    domain_ip: str = Field(alias="domainIp")
    port: int = Field(ge=1, le=65536)


class EmailNotificationSettings(BaseModel):
    enabled: Optional[bool] = False


class HardwareRootCA(BaseModel):
    hardware_certificate: Optional[str] = Field(default=None, alias="hardwareCertificate")
    control_connection_up: Optional[bool] = Field(default=False, alias="controlConnectionUp")


class Certificate(BaseModel):
    certificate_signing: str = Field(alias="certificateSigning")
    validity_period: str = Field(alias="validityPeriod")
    retrieve_interval: str = Field(alias="retrieveInterval")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    email: Optional[str] = Field(default=None)


class VEdgeCloud(BaseModel):
    certificateauthority: Optional[str] = None


class Banner(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.off


class ProxyHTTPServer(BaseModel):
    proxy: bool
    proxy_ip: str = Field(default="", alias="proxyIp")
    proxy_port: str = Field(default="", alias="proxyPort")


class ReverseProxy(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.off


class CloudX(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.off


class ManageEncryptedPassword(BaseModel):
    manage_type8_password: Optional[bool] = Field(default=False, alias="manageType8Password")


class CloudServices(BaseModel):
    enabled: Optional[bool] = False
    vanalytics_enabled: Optional[bool] = Field(default=False, alias="vanalyticsEnabled")
    vmonitoring_enabled: Optional[bool] = Field(default=False, alias="vmonitoringEnabled")
    otp: Optional[str] = None
    cloud_gateway_url: Optional[str] = Field(default=None, alias="cloudGatewayUrl")
    vanalytics_enabled_time: Optional[datetime.datetime] = Field(default=None, alias="vanalyticsEnabledTime")
    vmonitoring_enabled_time: Optional[datetime.datetime] = Field(default=None, alias="vmonitoringEnabledTime")


class ClientSessionTimeout(BaseModel):
    isEnabled: Optional[bool] = Field(default=False, alias="isEnabled")
    timeout: Optional[int] = Field(default=None, ge=10, description="timeout in minutes")


class SessionLifeTime(BaseModel):
    session_life_time: int = Field(alias="sessionLifeTime", ge=30, description="timeout in minutes")


class ServerSessionTimeout(BaseModel):
    server_session_timeout: int = Field(alias="serverSessionTimeout", ge=10, description="timeout in minutes")


class MaxSessionsPerUser(BaseModel):
    max_sessions_per_user: int = Field(alias="maxSessionsPerUser", ge=1)


class PasswordPolicy(BaseModel):
    password_policy: bool = Field(alias="passwordPolicy")
    password_expiration_time: Optional[int] = Field(
        default=False, alias="passwordExpirationTime", ge=1, description="timeout in days"
    )


class VManageDataStream(BaseModel):
    enable: Optional[bool] = False
    ip_type: Optional[DataStreamIPTypeEnum] = Field(default=None, alias="ipType")
    server_host_name: Union[IPvAnyAddress, DataStreamIPTypeEnum, None] = Field(default=None, alias="serverHostName")
    vpn: Optional[int] = Field(default=None, le=512)


class DataCollectionOnNotification(BaseModel):
    enabled: bool


class SDWANTelemetry(BaseModel):
    enabled: bool


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

    @request(get, "/settings/configuration/cloudservices", "data")
    def get_cloudservices(self) -> DataSequence[CloudServices]:
        ...

    @request(get, "/settings/configuration/clientSessionTimeout", "data")
    def get_client_session_timeout(self) -> DataSequence[ClientSessionTimeout]:
        ...

    @request(get, "/settings/configuration/sessionLifeTime", "data")
    def get_session_life_time(self) -> DataSequence[SessionLifeTime]:
        ...

    @request(get, "/settings/configuration/serverSessionTimeout", "data")
    def get_server_session_timeout(self) -> DataSequence[ServerSessionTimeout]:
        ...

    @request(get, "/settings/configuration/maxSessionsPerUser", "data")
    def get_max_sessions_per_user(self) -> DataSequence[MaxSessionsPerUser]:
        ...

    @request(get, "/settings/configuration/passwordPolicy", "data")
    def get_password_policy(self) -> DataSequence[PasswordPolicy]:
        ...

    @request(get, "/settings/configuration/vmanagedatastream", "data")
    def get_vmanage_data_stream(self) -> DataSequence[VManageDataStream]:
        ...

    @request(get, "/settings/configuration/dataCollectionOnNotification", "data")
    def get_data_collection_on_notification(self) -> DataSequence[DataCollectionOnNotification]:
        ...

    @request(get, "/settings/configuration/sdWanTelemetry", "data")
    def get_sdwan_telemetry(self) -> DataSequence[SDWANTelemetry]:
        ...

    def get_google_map_key(self):
        # GET /settings/configuration/googleMapKey
        ...

    def get_maintenance_window(self):
        # GET /settings/configuration/maintenanceWindow
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
