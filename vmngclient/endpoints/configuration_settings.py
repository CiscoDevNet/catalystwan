# mypy: disable-error-code="empty-body"
import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, IPvAnyAddress

from vmngclient.endpoints import APIEndpoints, get
from vmngclient.typed_list import DataSequence


class ModeEnum(str, Enum):
    on = "on"
    off = "off"


class DataStreamIPTypeEnum(str, Enum):
    system = "systemIp"
    mgmt = "mgmtIp"
    transport = "transportIp"


class PasswordPolicyEnum(str, Enum):
    disabled = "disabled"
    medium = "mediumSecurity"
    high = "highSecurity"


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
    is_enabled: Optional[bool] = Field(default=False, alias="isEnabled")
    timeout: Optional[int] = Field(default=None, ge=10, description="timeout in minutes")


class SessionLifeTime(BaseModel):
    session_life_time: int = Field(alias="sessionLifeTime", ge=30, description="timeout in minutes")


class ServerSessionTimeout(BaseModel):
    server_session_timeout: int = Field(alias="serverSessionTimeout", ge=10, description="timeout in minutes")


class MaxSessionsPerUser(BaseModel):
    max_sessions_per_user: int = Field(alias="maxSessionsPerUser", ge=1)


class PasswordPolicy(BaseModel):
    password_policy: Union[bool, PasswordPolicyEnum] = Field(alias="passwordPolicy")
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


class StatsOperation(BaseModel):
    stats_operation: str = Field(alias="statsOperation")
    rid: int = Field(alias="@rid")
    operation_interval: int = Field(alias="operationInterval", ge=1, description="interval in minutes")
    default_interval: int = Field(alias="defaultInterval", ge=1, description="interval in minutes")


class MaintenanceWindow(BaseModel):
    enabled: Optional[bool] = False
    message: Optional[str] = ""
    start: Optional[datetime.datetime] = Field(default=None, alias="epochStartTimeInMillis")
    end: Optional[datetime.datetime] = Field(default=None, alias="epochEndTimeInMillis")


class ElasticSearchDBSize(BaseModel):
    index_name: str = Field(alias="indexName")
    size_in_gb: int = Field(alias="sizeInGB")


class GoogleMapKey(BaseModel):
    key: str


class SoftwareInstallTimeout(BaseModel):
    download_timeout: int = Field(alias="downloadTimeoutInMin", ge=60)
    activate_timeout: int = Field(alias="activateTimeoutInMin", ge=30)


class IPSSignatureSettings(BaseModel):
    is_enabled: Optional[bool] = Field(default=False, alias="isEnabled")
    username: Optional[str] = None
    update_interval: Optional[int] = Field(
        default=None, alias="updateInterval", description="interval in minutes", ge=1, le=1440
    )


class SmartAccountCredentials(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class PnPConnectSync(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.off


class ClaimDevice(BaseModel):
    enabled: bool


class WalkMe(BaseModel):
    walkme: bool
    walkme_analytics: bool = Field(alias="walkmeAnalytics")


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

    @get("/settings/configuration/{setting_type}")
    def get_configuration_by_setting_type(self, setting_type: str) -> dict:
        ...

    @get("/settings/configuration/organization", "data")
    def get_organizations(self) -> DataSequence[Organization]:
        ...

    @get("/settings/configuration/device", "data")
    def get_devices(self) -> DataSequence[Device]:
        ...

    @get("/settings/configuration/emailNotificationSettings", "data")
    def get_email_notification_settings(self) -> DataSequence[EmailNotificationSettings]:
        ...

    @get("/settings/configuration/hardwarerootca", "data")
    def get_hardware_root_cas(self) -> DataSequence[HardwareRootCA]:
        ...

    @get("/settings/configuration/certificate", "data")
    def get_certificates(self) -> DataSequence[Certificate]:
        ...

    @get("/settings/configuration/vedgecloud", "data")
    def get_vedge_cloud(self) -> DataSequence[VEdgeCloud]:
        ...

    @get("/settings/configuration/banner", "data")
    def get_banners(self) -> DataSequence[Banner]:
        ...

    @get("/settings/configuration/proxyHttpServer", "data")
    def get_proxy_http_servers(self) -> DataSequence[ProxyHTTPServer]:
        ...

    @get("/settings/configuration/reverseproxy", "data")
    def get_reverse_proxies(self) -> DataSequence[ReverseProxy]:
        ...

    @get("/settings/configuration/cloudx", "data")
    def get_cloudx(self) -> DataSequence[CloudX]:
        ...

    @get("/settings/configuration/manageEncryptedPassword", "data")
    def get_manage_encrypted_password(self) -> DataSequence[ManageEncryptedPassword]:
        ...

    @get("/settings/configuration/cloudservices", "data")
    def get_cloudservices(self) -> DataSequence[CloudServices]:
        ...

    @get("/settings/configuration/clientSessionTimeout", "data")
    def get_client_session_timeout(self) -> DataSequence[ClientSessionTimeout]:
        ...

    @get("/settings/configuration/sessionLifeTime", "data")
    def get_session_life_time(self) -> DataSequence[SessionLifeTime]:
        ...

    @get("/settings/configuration/serverSessionTimeout", "data")
    def get_server_session_timeout(self) -> DataSequence[ServerSessionTimeout]:
        ...

    @get("/settings/configuration/maxSessionsPerUser", "data")
    def get_max_sessions_per_user(self) -> DataSequence[MaxSessionsPerUser]:
        ...

    @get("/settings/configuration/passwordPolicy", "data")
    def get_password_policy(self) -> DataSequence[PasswordPolicy]:
        ...

    @get("/settings/configuration/vmanagedatastream", "data")
    def get_vmanage_data_stream(self) -> DataSequence[VManageDataStream]:
        ...

    @get("/settings/configuration/dataCollectionOnNotification", "data")
    def get_data_collection_on_notification(self) -> DataSequence[DataCollectionOnNotification]:
        ...

    @get("/settings/configuration/sdWanTelemetry", "data")
    def get_sdwan_telemetry(self) -> DataSequence[SDWANTelemetry]:
        ...

    @get("/management/statsconfig")
    def get_stats_config(self) -> DataSequence[StatsOperation]:
        ...

    @get("/settings/configuration/spMetadata")
    def get_sp_metadata(self) -> str:
        ...

    @get("/management/elasticsearch/index/size", "indexSize")
    def get_elasticsearch_db_size(self) -> DataSequence[ElasticSearchDBSize]:
        ...

    @get("/settings/configuration/googleMapKey", "data")
    def get_google_map_key(self) -> DataSequence[GoogleMapKey]:
        ...

    @get("/settings/configuration/maintenanceWindow", "data")
    def get_maintenance_window(self) -> DataSequence[MaintenanceWindow]:
        ...

    @get("/settings/configuration/softwareMaintenance", "data")
    def get_software_install_timeout(self) -> DataSequence[SoftwareInstallTimeout]:
        ...

    @get("/settings/configuration/credentials", "data")
    def get_ips_signature_settings(self) -> DataSequence[IPSSignatureSettings]:
        ...

    @get("/settings/configuration/smartaccountcredentials", "data")
    def get_smart_account_credentials(self) -> DataSequence[SmartAccountCredentials]:
        ...

    @get("/settings/configuration/pnpConnectSync", "data")
    def get_pnp_connect_sync(self) -> DataSequence[PnPConnectSync]:
        ...

    @get("/settings/configuration/claimDevice", "data")
    def get_claim_device(self) -> DataSequence[ClaimDevice]:
        ...

    @get("/settings/configuration/walkme", "data")
    def get_walkme(self) -> DataSequence[WalkMe]:
        ...

    def new_cert_configuration(self):
        # POST /settings/configuration/certificate/{settingType}
        ...

    def new_configuration(self):
        # POST /settings/configuration/{settingType}
        ...
