# mypy: disable-error-code="empty-body"
import datetime
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic.v1 import BaseModel, Field, IPvAnyAddress, validator

from vmngclient.endpoints import JSON, APIEndpoints, get, post, put, view
from vmngclient.typed_list import DataSequence
from vmngclient.utils.session_type import ProviderView, SingleTenantView


class ModeEnum(str, Enum):
    ON = "on"
    OFF = "off"


class DataStreamIPTypeEnum(str, Enum):
    SYSTEM = "systemIp"
    MGMT = "mgmtIp"
    TRANSPORT = "transportIp"


class PasswordPolicyEnum(str, Enum):
    DISABLED = "disabled"
    MEDIUM = "mediumSecurity"
    HIGH = "highSecurity"


class SmartLicensingSettingModeEnum(str, Enum):
    ONPREM = "on-prem"
    OFFLINE = "offline"
    ONLINE = "online"


class CRLActionEnum(str, Enum):
    DISABLE = "disable"
    REVOKE = "revoke"
    QUARANTINE = "quarantine"


class Organization(BaseModel):
    class Config:
        allow_population_by_field_name = True

    org: Optional[str] = Field(default=None)
    domain_id: Optional[str] = Field(alias="domain-id")
    control_connection_up: Optional[bool] = Field(alias="controlConnectionUp")


class Device(BaseModel):
    class Config:
        allow_population_by_field_name = True

    domain_ip: Optional[str] = Field(default=None, alias="domainIp")
    port: Optional[int] = Field(default=None, ge=1, le=65536)


class EmailNotificationSettings(BaseModel):
    enabled: Optional[bool] = False


class HardwareRootCA(BaseModel):
    class Config:
        allow_population_by_field_name = True

    hardware_certificate: Optional[str] = Field(default=None, alias="hardwareCertificate")
    control_connection_up: Optional[bool] = Field(default=False, alias="controlConnectionUp")


class Certificate(BaseModel):
    class Config:
        allow_population_by_field_name = True

    certificate_signing: str = Field(alias="certificateSigning")
    validity_period: str = Field(alias="validityPeriod")
    retrieve_interval: str = Field(alias="retrieveInterval")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    email: Optional[str] = Field(default=None)


class VEdgeCloud(BaseModel):
    certificateauthority: Optional[str] = None


class Banner(BaseModel):
    class Config:
        allow_population_by_field_name = True

    mode: Optional[ModeEnum] = ModeEnum.OFF
    banner_detail: Optional[str] = Field(alias="bannerDetail")


class ProxyHTTPServer(BaseModel):
    class Config:
        allow_population_by_field_name = True

    proxy: bool
    proxy_ip: str = Field(default="", alias="proxyIp")
    proxy_port: str = Field(default="", alias="proxyPort")


class ReverseProxy(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.OFF


class CloudX(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.OFF


class ManageEncryptedPassword(BaseModel):
    class Config:
        allow_population_by_field_name = True

    manage_type8_password: Optional[bool] = Field(default=False, alias="manageType8Password")


class CloudServices(BaseModel):
    class Config:
        allow_population_by_field_name = True

    enabled: Optional[bool] = False
    vanalytics_enabled: Optional[bool] = Field(default=False, alias="vanalyticsEnabled")
    vmonitoring_enabled: Optional[bool] = Field(default=False, alias="vmonitoringEnabled")
    otp: Optional[str] = None
    cloud_gateway_url: Optional[str] = Field(default=None, alias="cloudGatewayUrl")
    vanalytics_enabled_time: Optional[datetime.datetime] = Field(default=None, alias="vanalyticsEnabledTime")
    vmonitoring_enabled_time: Optional[datetime.datetime] = Field(default=None, alias="vmonitoringEnabledTime")


class ClientSessionTimeout(BaseModel):
    class Config:
        allow_population_by_field_name = True

    is_enabled: Optional[bool] = Field(default=False, alias="isEnabled")
    timeout: Optional[int] = Field(default=None, ge=10, description="timeout in minutes")


class SessionLifeTime(BaseModel):
    class Config:
        allow_population_by_field_name = True

    session_life_time: int = Field(alias="sessionLifeTime", ge=30, le=10080, description="lifetime in minutes")


class ServerSessionTimeout(BaseModel):
    class Config:
        allow_population_by_field_name = True

    server_session_timeout: int = Field(alias="serverSessionTimeout", ge=10, le=30, description="timeout in minutes")


class MaxSessionsPerUser(BaseModel):
    class Config:
        allow_population_by_field_name = True

    max_sessions_per_user: int = Field(alias="maxSessionsPerUser", ge=1, le=8)


class PasswordPolicy(BaseModel):
    class Config:
        allow_population_by_field_name = True

    password_policy: Union[bool, PasswordPolicyEnum] = Field(alias="passwordPolicy")
    password_expiration_time: Optional[int] = Field(
        default=False, alias="passwordExpirationTime", ge=1, le=90, description="timeout in days"
    )


class VManageDataStream(BaseModel):
    class Config:
        allow_population_by_field_name = True

    enable: Optional[bool] = False
    ip_type: Optional[DataStreamIPTypeEnum] = Field(default=None, alias="ipType")
    server_host_name: Union[IPvAnyAddress, DataStreamIPTypeEnum, None] = Field(default=None, alias="serverHostName")
    vpn: Optional[int] = Field(default=None, le=512)


class DataCollectionOnNotification(BaseModel):
    enabled: bool


class SDWANTelemetry(BaseModel):
    enabled: bool


class StatsOperation(BaseModel):
    class Config:
        allow_population_by_field_name = True

    stats_operation: str = Field(alias="statsOperation")
    rid: int = Field(alias="@rid")
    operation_interval: int = Field(alias="operationInterval", ge=1, description="interval in minutes")
    default_interval: int = Field(alias="defaultInterval", ge=1, description="interval in minutes")


class MaintenanceWindow(BaseModel):
    class Config:
        allow_population_by_field_name = True

    enabled: Optional[bool] = False
    message: Optional[str] = ""
    start: Optional[int] = Field(default=None, alias="epochStartTimeInMillis")
    end: Optional[int] = Field(default=None, alias="epochEndTimeInMillis")


class ElasticSearchDBSize(BaseModel):
    class Config:
        allow_population_by_field_name = True

    index_name: str = Field(alias="indexName")
    size_in_gb: int = Field(alias="sizeInGB")


class GoogleMapKey(BaseModel):
    key: str


class SoftwareInstallTimeout(BaseModel):
    class Config:
        allow_population_by_field_name = True

    download_timeout: str = Field(alias="downloadTimeoutInMin")
    activate_timeout: str = Field(alias="activateTimeoutInMin")
    control_pps: Optional[str] = Field(alias="controlPps")

    @validator("download_timeout")
    def check_download_timeout(cls, download_timeout_str: str):
        download_timeout = int(download_timeout_str)
        if download_timeout < 60 or download_timeout > 360:
            raise ValueError("download timeout should be in range 60-360")
        return download_timeout_str

    @validator("activate_timeout")
    def check_activate_timeout(cls, activate_timeout_str: str):
        activate_timeout = int(activate_timeout_str)
        if activate_timeout < 60 or activate_timeout > 180:
            raise ValueError("activate timeout should be in range 30-180")
        return activate_timeout_str

    @validator("control_pps")
    def check_control_pps(cls, control_pps_str: str):
        control_pps = int(control_pps_str)
        if control_pps < 300 or control_pps > 65535:
            raise ValueError("control pps should be in range 300-65535")
        return control_pps_str


class IPSSignatureSettings(BaseModel):
    class Config:
        allow_population_by_field_name = True

    is_enabled: Optional[bool] = Field(default=False, alias="isEnabled")
    username: Optional[str] = None
    update_interval: Optional[int] = Field(
        default=None, alias="updateInterval", description="interval in minutes", ge=1, le=1440
    )


class SmartAccountCredentials(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class PnPConnectSync(BaseModel):
    mode: Optional[ModeEnum] = ModeEnum.OFF


class ClaimDevice(BaseModel):
    enabled: bool


class WalkMe(BaseModel):
    class Config:
        allow_population_by_field_name = True

    walkme: bool
    walkme_analytics: bool = Field(alias="walkmeAnalytics")


class SmartLicensingSetting(BaseModel):
    class Config:
        allow_population_by_field_name = True

    mode: Optional[SmartLicensingSettingModeEnum] = None
    ssm_server_url: Optional[str] = Field(None, alias="ssmServerUrl")
    ssm_client_id: Optional[str] = Field(None, alias="ssmClientId")
    ssm_client_secret: Optional[str] = Field(None, alias="ssmClientSecret")


class StatsCollectionInterval(BaseModel):
    class Config:
        allow_population_by_field_name = True

    config_name: Literal["statsCollection"] = Field(default="statsCollection", alias="configName")
    operation_interval: int = Field(
        ge=5, le=180, alias="operationInterval", desctiption="collecion interval in minutes"
    )


StatsConfigItem = Union[StatsCollectionInterval, None]  # open for extension for now only one option could be deduced


class StatsConfig(BaseModel):
    config: List[StatsConfigItem]

    @staticmethod
    def from_collection_interval(interval: int) -> "StatsConfig":
        return StatsConfig(config=[StatsCollectionInterval(operationInterval=interval)])


class CRLSettings(BaseModel):
    class Config:
        allow_population_by_field_name = True

    action: CRLActionEnum
    crl_url: Optional[str] = Field(None, alias="crlUrl")
    polling_interval: Optional[str] = Field(description="Retrieval interval (1-24 hours)")
    vpn: Optional[str]

    @validator("polling_interval")
    def check_polling_interval(cls, polling_interval_str: str):
        polling_interval = int(polling_interval_str)
        if polling_interval < 1 or polling_interval > 24:
            raise ValueError("Polling interval should be in range 1-24")
        return polling_interval_str

    @validator("vpn")
    def check_vpn(cls, vpn_str: str):
        vpn = int(vpn_str)
        if vpn < 0 or vpn > 65530:
            raise ValueError("vpn should be in range 0-65530")
        return vpn_str


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

    def get_cert_configuration(self):
        # GET /settings/configuration/certificate/{settingType}
        ...

    @get("/settings/configuration/{setting_type}")
    def get_configuration_by_setting_type(self, setting_type: str) -> JSON:
        ...

    @get("/settings/configuration/organization", "data")
    def get_organizations(self) -> DataSequence[Organization]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/device", "data")
    def get_devices(self) -> DataSequence[Device]:
        ...

    @get("/settings/configuration/emailNotificationSettings", "data")
    def get_email_notification_settings(self) -> DataSequence[EmailNotificationSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/hardwarerootca", "data")
    def get_hardware_root_cas(self) -> DataSequence[HardwareRootCA]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/certificate", "data")
    def get_certificates(self) -> DataSequence[Certificate]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/vedgecloud", "data")
    def get_vedge_cloud(self) -> DataSequence[VEdgeCloud]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/crlSetting")
    def get_clr_settings(self) -> DataSequence[CRLSettings]:
        ...

    @get("/settings/configuration/banner", "data")
    def get_banner(self) -> DataSequence[Banner]:
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

    @view({SingleTenantView, ProviderView})
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

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/vmanagedatastream", "data")
    def get_vmanage_data_stream(self) -> DataSequence[VManageDataStream]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/dataCollectionOnNotification", "data")
    def get_data_collection_on_notification(self) -> DataSequence[DataCollectionOnNotification]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/sdWanTelemetry", "data")
    def get_sdwan_telemetry(self) -> DataSequence[SDWANTelemetry]:
        ...

    @view({SingleTenantView, ProviderView})
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

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/maintenanceWindow", "data")
    def get_maintenance_window(self) -> DataSequence[MaintenanceWindow]:
        ...

    @get("/settings/configuration/softwareMaintenance", "data")
    def get_software_install_timeout(self) -> DataSequence[SoftwareInstallTimeout]:
        ...

    @get("/settings/configuration/credentials", "data")
    def get_ips_signature_settings(self) -> DataSequence[IPSSignatureSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/smartaccountcredentials", "data")
    def get_smart_account_credentials(self) -> DataSequence[SmartAccountCredentials]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/pnpConnectSync", "data")
    def get_pnp_connect_sync(self) -> DataSequence[PnPConnectSync]:
        ...

    @get("/settings/configuration/claimDevice", "data")
    def get_claim_device(self) -> DataSequence[ClaimDevice]:
        ...

    @get("/settings/configuration/walkme", "data")
    def get_walkme(self) -> DataSequence[WalkMe]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/smartLicensing", "data")
    def get_smart_licensing_settings(self) -> DataSequence[SmartLicensingSetting]:
        ...

    def new_cert_configuration(self):
        # POST /settings/configuration/certificate/{settingType}
        ...

    def new_configuration(self):
        # POST /settings/configuration/{settingType}
        ...

    @put("/settings/configuration/{setting_type}")
    def edit_configuration_by_setting_type(self, setting_type: str, payload: JSON) -> JSON:
        ...

    @put("/settings/configuration/organization", "data")
    def edit_organizations(self, payload: Organization) -> DataSequence[Organization]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/device", "data")
    def edit_devices(self, payload: Device) -> DataSequence[Device]:
        ...

    @put("/settings/configuration/emailNotificationSettings", "data")
    def edit_email_notification_settings(
        self, payload: EmailNotificationSettings
    ) -> DataSequence[EmailNotificationSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/hardwarerootca", "data")
    def edit_hardware_root_cas(self, payload: HardwareRootCA) -> DataSequence[HardwareRootCA]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/certificate", "data")
    def edit_certificates(self, payload: Certificate) -> DataSequence[Certificate]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/vedgecloud", "data")
    def edit_vedge_cloud(self, payload: VEdgeCloud) -> DataSequence[VEdgeCloud]:
        ...

    @put("/settings/configuration/banner", "data")
    def edit_banner(self, payload: Banner) -> DataSequence[Banner]:
        ...

    @put("/settings/configuration/proxyHttpServer", "data")
    def edit_proxy_http_servers(self, payload: ProxyHTTPServer) -> DataSequence[ProxyHTTPServer]:
        ...

    @put("/settings/configuration/reverseproxy", "data")
    def edit_reverse_proxies(self, payload: ReverseProxy) -> DataSequence[ReverseProxy]:
        ...

    @put("/settings/configuration/cloudx", "data")
    def edit_cloudx(self, payload: CloudX) -> DataSequence[CloudX]:
        ...

    @put("/settings/configuration/manageEncryptedPassword", "data")
    def edit_manage_encrypted_password(self, payload: ManageEncryptedPassword) -> DataSequence[ManageEncryptedPassword]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/cloudservices", "data")
    def edit_cloudservices(self, payload: CloudServices) -> DataSequence[CloudServices]:
        ...

    @put("/settings/configuration/clientSessionTimeout", "data")
    def edit_client_session_timeout(self, payload: ClientSessionTimeout) -> DataSequence[ClientSessionTimeout]:
        ...

    @put("/settings/configuration/sessionLifeTime", "data")
    def edit_session_life_time(self, payload: SessionLifeTime) -> DataSequence[SessionLifeTime]:
        ...

    @put("/settings/configuration/serverSessionTimeout", "data")
    def edit_server_session_timeout(self, payload: ServerSessionTimeout) -> DataSequence[ServerSessionTimeout]:
        ...

    @put("/settings/configuration/maxSessionsPerUser", "data")
    def edit_max_sessions_per_user(self, payload: MaxSessionsPerUser) -> DataSequence[MaxSessionsPerUser]:
        ...

    @put("/settings/configuration/passwordPolicy", "data")
    def edit_password_policy(self, payload: PasswordPolicy) -> DataSequence[PasswordPolicy]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/vmanagedatastream", "data")
    def edit_vmanage_data_stream(self, payload: VManageDataStream) -> DataSequence[VManageDataStream]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/dataCollectionOnNotification", "data")
    def edit_data_collection_on_notification(
        self, payload: DataCollectionOnNotification
    ) -> DataSequence[DataCollectionOnNotification]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/sdWanTelemetry", "data")
    def edit_sdwan_telemetry(self, payload: SDWANTelemetry) -> DataSequence[SDWANTelemetry]:
        ...

    @view({SingleTenantView, ProviderView})
    @post("/management/statsconfig")
    def edit_stats_config(self, payload: StatsConfig) -> DataSequence[StatsOperation]:
        ...

    @put("/settings/configuration/spMetadata")
    def edit_sp_metadata(self, payload: str) -> str:
        ...

    @put("/management/elasticsearch/index/size", "indexSize")
    def edit_elasticsearch_db_size(self, payload: ElasticSearchDBSize) -> DataSequence[ElasticSearchDBSize]:
        ...

    @put("/settings/configuration/googleMapKey")
    def edit_google_map_key(self, payload: GoogleMapKey) -> DataSequence[GoogleMapKey]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/maintenanceWindow")
    def edit_maintenance_window(self, payload: MaintenanceWindow) -> DataSequence[MaintenanceWindow]:
        ...

    @put("/settings/configuration/softwareMaintenance", "data")
    def edit_software_install_timeout(self, payload: SoftwareInstallTimeout) -> DataSequence[SoftwareInstallTimeout]:
        ...

    @put("/settings/configuration/credentials", "data")
    def edit_ips_signature_settings(self, payload: IPSSignatureSettings) -> DataSequence[IPSSignatureSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/smartaccountcredentials", "data")
    def edit_smart_account_credentials(self, payload: SmartAccountCredentials) -> DataSequence[SmartAccountCredentials]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/pnpConnectSync", "data")
    def edit_pnp_connect_sync(self, payload: PnPConnectSync) -> DataSequence[PnPConnectSync]:
        ...

    @put("/settings/configuration/claimDevice", "data")
    def edit_claim_device(self, payload: ClaimDevice) -> DataSequence[ClaimDevice]:
        ...

    @put("/settings/configuration/walkme", "data")
    def edit_walkme(self, payload: WalkMe) -> DataSequence[WalkMe]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/smartLicensing", "data")
    def edit_smart_licensing_settings(self, payload: SmartLicensingSetting) -> DataSequence[SmartLicensingSetting]:
        ...
