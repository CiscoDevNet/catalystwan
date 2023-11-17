import datetime as dt
from typing import List, Optional

from attr import define, field  # type: ignore
from pydantic.v1 import BaseModel, Field

from vmngclient.exceptions import RetrieveIntervalOutOfRange
from vmngclient.utils.alarm_status import Severity
from vmngclient.utils.certificate_status import ValidityPeriod
from vmngclient.utils.colors import PrintColors
from vmngclient.utils.creation_tools import FIELD_NAME, asdict, convert_attributes
from vmngclient.utils.personality import Personality
from vmngclient.utils.reachability import Reachability
from vmngclient.utils.template_type import TemplateType


class DataclassBase:
    def __str__(self):
        return (
            f"{self.__class__.__name__}(\n"
            + "\n".join(f"    {attribute[0]}: {attribute[1]}, " for attribute in asdict(self).items())
            + "\n)"
        )


@define(frozen=True, field_transformer=convert_attributes)
class AdminTech(DataclassBase):
    creation_time: dt.datetime = field(metadata={FIELD_NAME: "creationTime"})
    size: int
    filename: str = field(metadata={FIELD_NAME: "fileName"})
    state: str
    device_ip: str = field(metadata={FIELD_NAME: "deviceIP"})
    system_ip: str = field(metadata={FIELD_NAME: "local-system-ip"})
    token_id: str = field(metadata={FIELD_NAME: "requestTokenId"})
    tac_state: Optional[str] = field(default=None)


@define(frozen=True, field_transformer=convert_attributes)
class DeviceAdminTech(DataclassBase):
    filename: str = field(metadata={FIELD_NAME: "fileName"})
    creation_time: dt.datetime = field(metadata={FIELD_NAME: "creationTime"})
    size: int
    state: str
    token_id: Optional[str] = field(default=None, metadata={FIELD_NAME: "requestTokenId"})


@define(frozen=True, field_transformer=convert_attributes)
class AlarmData(DataclassBase):
    severity: Severity = field(converter=Severity, default=None)
    component: Optional[str] = field(default=None)
    active: Optional[bool] = field(default=None)
    severity_number: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None, metadata={FIELD_NAME: "type"})
    system_ip: Optional[str] = field(default=None, metadata={FIELD_NAME: "system-ip"})
    hostname: Optional[str] = field(default=None, metadata={FIELD_NAME: "host-name"})
    site_id: Optional[str] = field(default=None, metadata={FIELD_NAME: "site-id"})
    new_state: Optional[str] = field(default=None, metadata={FIELD_NAME: "new-state"})
    interface_name: Optional[str] = field(default=None, metadata={FIELD_NAME: "if-name"})
    vpn_id: Optional[str] = field(default=None, metadata={FIELD_NAME: "vpn-id"})
    viewed: Optional[bool] = field(default=None, metadata={FIELD_NAME: "acknowledged"})
    message: Optional[str] = field(default=None)
    values: Optional[list] = field(default=None)
    values_short_display: Optional[list] = field(default=None)
    event_name: Optional[str] = field(default=None, metadata={FIELD_NAME: "eventname"})
    rule_name: Optional[str] = field(default=None, metadata={FIELD_NAME: "rulename"})
    entry_time: Optional[int] = field(default=None)
    receive_time: Optional[int] = field(default=None)
    rule_name_display: Optional[str] = field(default=None)
    uuid: Optional[str] = field(default=None)
    possible_causes: Optional[List[str]] = field(default=None)
    consumed_events: Optional[list] = field(default=None)
    devices: Optional[list] = field(default=None)
    tenant: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)

    def issubset(self, other: "AlarmData") -> bool:
        field_keys = {field_key for field_key in self.__annotations__ if getattr(self, field_key)}
        return all(getattr(self, field_key) == getattr(other, field_key) for field_key in field_keys)

    def lowercase(self) -> "AlarmData":
        data = dict()
        for field_key in self.__annotations__:
            attr = getattr(self, field_key)
            try:
                data[field_key] = attr.lower()
            except AttributeError:
                data[field_key] = attr

        return AlarmData(**data)

    def alarm_severity_print(self) -> str:
        color = {
            Severity.CRITICAL: PrintColors.RED,
            Severity.MAJOR: PrintColors.YELLOW,
            Severity.MEDIUM: PrintColors.BLUE,
            Severity.MINOR: PrintColors.GREEN,
            Severity.UNKNOWN: PrintColors.NONE,
        }

        return f"{color[self.severity].value}{self.severity}{PrintColors.NONE.value}"

    def format_datetime(self, time: int) -> str:
        if time is None:
            return "N/A"
        return dt.datetime.fromtimestamp(time / 1e3).strftime("%H:%M:%S %Y-%m-%d")

    def __str__(self):
        result = (
            f"{self.__class__.__name__}: \n    "
            f"{self.message}\n    "
            f"{self.alarm_severity_print()}\n    "
            f"Alarm received at {self.format_datetime(self.receive_time)} "
            f"(entry time: {self.format_datetime(self.entry_time)}).\n    "
            f"Device {self.hostname} (system ip: {self.system_ip}).\n    "
            f"Alarm type: {self.name}."
        )
        return result


@define
class Device(DataclassBase):
    uuid: str
    personality: Personality = field(converter=Personality)
    id: str = field(metadata={FIELD_NAME: "deviceId"})
    hostname: str = field(metadata={FIELD_NAME: "host-name"})
    reachability: Reachability = field(converter=Reachability)
    local_system_ip: str = field(metadata={FIELD_NAME: "local-system-ip"})
    status: Optional[str] = field(default=None)
    memUsage: Optional[float] = field(default=None)
    mem_state: Optional[str] = field(default=None, metadata={FIELD_NAME: "memState"})
    cpu_state: Optional[str] = field(default=None, metadata={FIELD_NAME: "cpuState"})
    cpu_load: Optional[float] = field(default=None, metadata={FIELD_NAME: "cpuLoad"})
    state_description: Optional[str] = field(default=None)
    connected_vManages: List[str] = field(factory=list, metadata={FIELD_NAME: "connectedVManages"})
    model: Optional[str] = field(default=None, metadata={FIELD_NAME: "device-model"})
    board_serial: Optional[str] = field(default=None, metadata={FIELD_NAME: "board-serial"})
    vedgeCertificateState: Optional[str] = field(default=None, metadata={FIELD_NAME: "vedgeCertificateState"})  # TODO
    chasis_number: Optional[str] = field(default=None, metadata={FIELD_NAME: "chasisNumber"})
    site_id: Optional[str] = field(default=None, metadata={FIELD_NAME: "site-id"})
    site_name: Optional[str] = field(default=None, metadata={FIELD_NAME: "site-name"})

    @property
    def is_reachable(self) -> bool:
        return self.reachability is Reachability.REACHABLE


@define
class WanInterface(DataclassBase):
    color: str
    vDeviceIp: str = field(metadata={FIELD_NAME: "vdevice-name"})
    vDeviceName: str = field(metadata={FIELD_NAME: "vdevice-host-name"})
    adminState: str = field(metadata={FIELD_NAME: "admin-state"})
    interfaceName: str = field(metadata={FIELD_NAME: "interface"})
    privateIp: str = field(metadata={FIELD_NAME: "private-ip"})
    publicIp: str = field(metadata={FIELD_NAME: "public-ip"})
    privatePort: int = field(metadata={FIELD_NAME: "private-port"})
    publicPort: int = field(metadata={FIELD_NAME: "public-port"})
    operationalState: str = field(metadata={FIELD_NAME: "operation-state"})


@define
class Connection(DataclassBase):
    state: str
    peerType: str = field(metadata={FIELD_NAME: "peer-type"})
    systemIp: str = field(metadata={FIELD_NAME: "system-ip"})


@define
class BfdSessionData(DataclassBase):
    state: str
    siteId: str = field(metadata={FIELD_NAME: "site-id"})
    sourceTlocColor: str = field(metadata={FIELD_NAME: "local-color"})
    remoteTlocColor: str = field(metadata={FIELD_NAME: "color"})
    deviceIp: str = field(metadata={FIELD_NAME: "system-ip"})
    sourceIp: str = field(metadata={FIELD_NAME: "src-ip"})
    destinationPublicIp: str = field(metadata={FIELD_NAME: "dst-ip"})


@define
class OmpPeerData(DataclassBase):
    type: str
    state: str
    peerIp: str = field(metadata={FIELD_NAME: "peer"})
    siteId: str = field(metadata={FIELD_NAME: "site-id"})
    domainId: str = field(metadata={FIELD_NAME: "domain-id"})
    deviceIp: str = field(metadata={FIELD_NAME: "vdevice-name"})


@define
class OmpReceivedRouteData(DataclassBase):
    protocol: str
    peerIp: str = field(metadata={FIELD_NAME: "from-peer"})


@define
class OmpAdvertisedRouteData(DataclassBase):
    protocol: str
    peerIp: str = field(metadata={FIELD_NAME: "to-peer"})


@define
class OmpReceivedTlocData(DataclassBase):
    peerIp: str = field(metadata={FIELD_NAME: "from-peer"})


@define
class OmpAdvertisedTlocData(DataclassBase):
    peerIp: str = field(metadata={FIELD_NAME: "to-peer"})


@define
class OmpServiceData(DataclassBase):
    name: str = field(metadata={FIELD_NAME: "service"})
    status: Optional[str] = field(default=None)


@define
class OmpSummaryData(DataclassBase):
    oper_state: str = field(metadata={FIELD_NAME: "operstate"})
    admin_state: str = field(metadata={FIELD_NAME: "adminstate"})
    routes_received: str = field(metadata={FIELD_NAME: "routes-received"})
    tlocs_received: str = field(metadata={FIELD_NAME: "tlocs-received"})
    routes_sent: str = field(metadata={FIELD_NAME: "routes-sent"})
    tlocs_installed: str = field(metadata={FIELD_NAME: "tlocs-installed"})
    tlocs_sent: str = field(metadata={FIELD_NAME: "tlocs-sent"})
    vsmart_peers: str = field(metadata={FIELD_NAME: "vsmart-peers"})


@define
class EventData(DataclassBase):
    system_ip: str
    vmanage_system_ip: str
    tenant: str
    device_type: str
    component: str
    severity_level: str
    host_name: str
    event: str
    details: str
    event_name: str = field(metadata={FIELD_NAME: "eventname"})


@define(frozen=True)
class User(DataclassBase):
    username: str = field(metadata={FIELD_NAME: "userName"})
    password: Optional[str] = field(default=None)
    group: List[str] = field(factory=list)
    locale: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    resource_group: Optional[str] = field(default=None, metadata={FIELD_NAME: "resGroupName"})


@define(kw_only=True)
class TemplateInfo(DataclassBase):
    last_updated_by: str = field(metadata={FIELD_NAME: "lastUpdatedBy"})
    id: str = field(metadata={FIELD_NAME: "templateId"})
    factory_default: bool = field(metadata={FIELD_NAME: "factoryDefault"})
    name: str = field(metadata={FIELD_NAME: "templateName"})
    devices_attached: int = field(metadata={FIELD_NAME: "devicesAttached"})
    description: str = field(metadata={FIELD_NAME: "templateDescription"})
    last_updated_on: dt.datetime = field(metadata={FIELD_NAME: "lastUpdatedOn"})
    resource_group: Optional[str] = field(default=None, metadata={FIELD_NAME: "resourceGroup"})


@define(kw_only=True)
class FeatureTemplateInfo(TemplateInfo):
    template_type: str = field(metadata={FIELD_NAME: "templateType"})
    device_type: List[str] = field(metadata={FIELD_NAME: "deviceType"})
    version: str = field(metadata={FIELD_NAME: "templateMinVersion"})
    template_definiton: Optional[str] = field(default=None, metadata={FIELD_NAME: "templateDefinition"})


@define(kw_only=True)
class DeviceTemplateInfo(TemplateInfo):
    device_type: str = field(metadata={FIELD_NAME: "deviceType"})
    template_class: str = field(metadata={FIELD_NAME: "templateClass"})
    config_type: TemplateType = field(converter=TemplateType, metadata={FIELD_NAME: "configType"})
    template_attached: int = field(metadata={FIELD_NAME: "templateAttached"})
    draft_mode: Optional[str] = field(default=None, metadata={FIELD_NAME: "draftMode"})
    device_role: Optional[str] = field(default=None, metadata={FIELD_NAME: "deviceRole"})


@define
class Speedtest(DataclassBase):
    device_ip: str
    device_name: str
    destination_ip: str
    destination_name: str
    status: str
    up_speed: float
    down_speed: float


@define(frozen=True)
class PacketSetup(DataclassBase):
    session_id: str = field(metadata={FIELD_NAME: "sessionId"})
    is_new_session: bool = field(metadata={FIELD_NAME: "isNewSession"})


@define(frozen=True)
class Status(DataclassBase):
    file_download_status: Optional[str] = field(default=None, metadata={FIELD_NAME: "fileDownloadStatus"})
    file_size: Optional[int] = field(default=None, metadata={FIELD_NAME: "fileSize"})


@define(frozen=True)
class ServiceConfigurationData(DataclassBase):
    """Administration -> Service Configuration"""

    vmanage_id: str = field(metadata={FIELD_NAME: "vmanageID"})
    device_ip: str = field(metadata={FIELD_NAME: "deviceIP"})  # consider using ip4 module to verify
    services: dict = field(metadata={FIELD_NAME: "services"})  # consider using nested dataclasses
    persona: str = field(default="COMPUTE_AND_DATA")  # TODO Enum
    username: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)


@define(frozen=True)
class CloudConnectorData(DataclassBase):
    """Administration -> Settings -> SD-AVC Cloud Connector"""

    client_id: str = field(metadata={FIELD_NAME: "clientId"})
    client_secret: str = field(metadata={FIELD_NAME: "clientSecret"})
    org_name: str = field(metadata={FIELD_NAME: "orgName"})
    telemetry_enabled: bool = field(metadata={FIELD_NAME: "telemetryEnabled"})
    affinity: Optional[str] = field(default=None)
    cloud_enabled: bool = field(default=True, metadata={FIELD_NAME: "cloudEnabled"})


@define(frozen=True)
class CloudServicesSettings(DataclassBase):
    """Administration -> Settings -> Cloud Services"""

    enabled: bool = field(metadata={FIELD_NAME: "enabled"})
    otp: Optional[str] = field(default=None, metadata={FIELD_NAME: "otp"})
    cloud_gateway_url: Optional[str] = field(default=None, metadata={FIELD_NAME: "cloudGatewayUrl"})


@define(frozen=True)
class CloudOnRampForSaasMode(DataclassBase):
    """
    Administration -> Settings -> Cloud on Ramp for Saas
    """

    mode: str = field(metadata={FIELD_NAME: "mode"})


@define(frozen=True)
class TLOC:
    color: str
    encapsulation: str


@define(frozen=True)
class TierInfo(DataclassBase):
    """Endpoint: /dataservice/tier

    Since vManage 20.12 version, object has been renamed to "Resource Profile".
    """

    name: str = field(metadata={FIELD_NAME: "tierName"})
    vpn: int
    rid: int = field(metadata={FIELD_NAME: "@rid"})
    ipv4_route_limit_type: Optional[str] = field(default=None, metadata={FIELD_NAME: "ipv4RouteLimitType"})
    ipv4_route_limit_threshold: Optional[int] = field(default=None, metadata={FIELD_NAME: "ipv4RouteLimitThreshold"})
    ipv4_route_limit: Optional[int] = field(default=None, metadata={FIELD_NAME: "ipv4RouteLimit"})
    ipv6_route_limit_type: Optional[str] = field(default=None, metadata={FIELD_NAME: "ipv6RouteLimitType"})
    ipv6_route_limit_threshold: Optional[int] = field(default=None, metadata={FIELD_NAME: "ipv6RouteLimitThreshold"})
    ipv6_route_limit: Optional[int] = field(default=None, metadata={FIELD_NAME: "ipv6RouteLimit"})
    tlocs: List[TLOC] = field(default=[])
    # New in 20.12 version
    nat_session_limit: Optional[int] = field(default=None, metadata={FIELD_NAME: "natSessionLimit"})


@define(frozen=True)
class FeatureTemplateInformation(DataclassBase):
    """Endpoint: /dataservice/template/feature"""

    id: str = field(metadata={FIELD_NAME: "templateId"})
    name: str = field(metadata={FIELD_NAME: "templateName"})
    description: str = field(metadata={FIELD_NAME: "templateDescription"})
    type: str = field(metadata={FIELD_NAME: "templateType"})  # TODO Enum
    device_types: List[str] = field(metadata={FIELD_NAME: "deviceType"})  # TODO Enum
    last_updated_by: str = field(metadata={FIELD_NAME: "lastUpdatedBy"})
    last_updated_on: dt.datetime = field(metadata={FIELD_NAME: "lastUpdatedOn"})
    factory_default: bool = field(metadata={FIELD_NAME: "factoryDefault"})
    devices_attached: int = field(metadata={FIELD_NAME: "devicesAttached"})
    attached_masters: int = field(metadata={FIELD_NAME: "attachedMastersCount"})
    version: str = field(metadata={FIELD_NAME: "templateMinVersion"})
    config_type: str = field(metadata={FIELD_NAME: "configType"})
    created_by: str = field(metadata={FIELD_NAME: "createdBy"})
    created_on: dt.datetime = field(metadata={FIELD_NAME: "createdOn"})
    resource_group: str = field(metadata={FIELD_NAME: "resourceGroup"})


@define
class Organization(DataclassBase):
    name: str = field(metadata={FIELD_NAME: "org"})
    domain_id: int = field(metadata={FIELD_NAME: "domain-id"})
    control_connection_up: Optional[bool] = field(default=None, metadata={FIELD_NAME: "controlConnectionUp"})


@define
class Password(DataclassBase):
    old_password: str = field(metadata={FIELD_NAME: "oldpassword"})
    new_password: str = field(metadata={FIELD_NAME: "newpassword"})


@define
class Certificate(DataclassBase):
    controller_certificate: str = field(metadata={FIELD_NAME: "certificateSigning"})
    first_name: str = field(metadata={FIELD_NAME: "firstName"})
    last_name: str = field(metadata={FIELD_NAME: "lastName"})
    email: str = field(metadata={FIELD_NAME: "email"})
    validity_period: ValidityPeriod = field(metadata={FIELD_NAME: "validityPeriod"})
    retrieve_interval: int = field(converter=str, metadata={FIELD_NAME: "retrieveInterval"})

    @retrieve_interval.validator  # type: ignore
    def retrieve_interval_is_valid(self, attribute, value):
        RETRIEVE_INTERVAL_MAX = 60
        RETRIEVE_INTERVAL_MIN = 1
        if not RETRIEVE_INTERVAL_MIN <= int(value) <= RETRIEVE_INTERVAL_MAX:
            raise RetrieveIntervalOutOfRange("Retrieve interval must be value between 1 and 60 minutes")


@define
class Vbond(DataclassBase):
    vbond_address: str = field(metadata={FIELD_NAME: "domainIp"})
    vbond_port: str = field(metadata={FIELD_NAME: "port"})


@define(frozen=True)
class TenantAAA(DataclassBase):
    """
    Provider-Tenant -> Tenant -> Administration -> Manage users -> Remote AAA
    """

    accounting: bool = field(metadata={FIELD_NAME: "accounting"})
    admin_auth_order: bool = field(metadata={FIELD_NAME: "adminAuthOrder"})
    audit_disable: bool = field(metadata={FIELD_NAME: "auditDisable"})
    auth_fallback: bool = field(metadata={FIELD_NAME: "authFallback"})
    auth_order: List[str] = field(metadata={FIELD_NAME: "authOrder"})


@define(frozen=True)
class RadiusServer(DataclassBase):
    """
    Provider-Tenant -> Tenant -> Administration -> Manage users -> Remote AAA -> RADIUS
    """

    address: str = field(metadata={FIELD_NAME: "address"})
    auth_port: int = field(metadata={FIELD_NAME: "authPort"})
    acct_port: int = field(metadata={FIELD_NAME: "acctPort"})
    vpn: int = field(metadata={FIELD_NAME: "vpn"})
    vpn_ip_subnet: str = field(metadata={FIELD_NAME: "vpnIpSubnet"})
    key: str = field(metadata={FIELD_NAME: "key"})
    secret_key: str = field(metadata={FIELD_NAME: "secretKey"})
    priority: int = field(metadata={FIELD_NAME: "priority"})


@define(frozen=True)
class TenantRadiusServer(DataclassBase):
    """
    Provider-Tenant -> Tenant -> Administration -> Manage users -> Remote AAA -> RADIUS
    """

    timeout: int = field(default=3, metadata={FIELD_NAME: "timeout"})
    retransmit: int = field(default=5, metadata={FIELD_NAME: "retransmit"})
    servers: List[RadiusServer] = field(factory=list, metadata={FIELD_NAME: "server"})


@define(frozen=True)
class TacacsServer(DataclassBase):
    """
    Provider-Tenant -> Tenant -> Administration -> Manage users -> Remote AAA -> TACACS server
    """

    address: str = field(metadata={FIELD_NAME: "address"})
    auth_port: int = field(metadata={FIELD_NAME: "authPort"})
    vpn: int = field(metadata={FIELD_NAME: "vpn"})
    vpn_ip_subnet: str = field(metadata={FIELD_NAME: "vpnIpSubnet"})
    key: str = field(metadata={FIELD_NAME: "key"})
    secret_key: str = field(metadata={FIELD_NAME: "secretKey"})
    priority: int = field(metadata={FIELD_NAME: "priority"})


@define(frozen=True)
class TenantTacacsServer(DataclassBase):
    """
    Provider-Tenant -> Tenant -> Administration -> Manage users -> Remote AAA -> TACACS server
    """

    timeout: int = field(default=3, metadata={FIELD_NAME: "timeout"})
    authentication: str = field(default="PAP", metadata={FIELD_NAME: "authentication"})
    servers: List[TacacsServer] = field(factory=list, metadata={FIELD_NAME: "server"})


@define
class SoftwareInstallTimeout(DataclassBase):
    download_timeout_min: int = field(converter=str, metadata={FIELD_NAME: "downloadTimeoutInMin"})
    activate_timeout_min: int = field(converter=str, metadata={FIELD_NAME: "activateTimeoutInMin"})


class FeatureTemplatesTypes(BaseModel):
    parent: str
    default: str
    display_name: str = Field(alias="displayName")
    name: str
    type_class: str = Field(alias="typeClass")
    description: str
    write_permission: bool
    read_permission: bool
    helper_type: List[str] = Field(default=[], alias="helperType")
    device_models: List[dict] = Field(default=[], alias="deviceModels")


@define
class ResourcePoolData(DataclassBase):
    """Endpoint: /resourcepool/resource/vpn"""

    tenant_id: str = field(metadata={FIELD_NAME: "tenantId"})
    tenant_vpn: int = field(metadata={FIELD_NAME: "tenantVpn"})
    device_vpn: Optional[int] = field(default=None, metadata={FIELD_NAME: "deviceVpn"})
