import datetime as dt
from typing import List, Optional

from attr import define, field  # type: ignore

from vmngclient.utils.creation_tools import FIELD_NAME, asdict, convert_attributes
from vmngclient.utils.device_model import DeviceModel
from vmngclient.utils.personality import Personality
from vmngclient.utils.reachability import Reachability


class DataclassBase:
    def __str__(self):
        return (
            f"{self.__class__.__name__}(\n"
            + "\n".join(f"    {attribute[0]}: {attribute[1]}," for attribute in asdict(self).items())
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
    component: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)
    active: Optional[bool] = field(default=None)
    name: Optional[str] = field(default=None, metadata={FIELD_NAME: "type"})
    system_ip: Optional[str] = field(default=None, metadata={FIELD_NAME: "system-ip"})
    hostname: Optional[str] = field(default=None, metadata={FIELD_NAME: "host-name"})
    site_id: Optional[str] = field(default=None, metadata={FIELD_NAME: "site-id"})
    new_state: Optional[str] = field(default=None, metadata={FIELD_NAME: "new-state"})
    interface_name: Optional[str] = field(default=None, metadata={FIELD_NAME: "if-name"})
    vpn_id: Optional[str] = field(default=None, metadata={FIELD_NAME: "vpn-id"})

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


@define
class Device(DataclassBase):
    uuid: str
    status: str
    personality: Personality = field(converter=Personality)
    id: str = field(metadata={FIELD_NAME: "deviceId"})
    hostname: str = field(metadata={FIELD_NAME: "host-name"})
    reachability: Reachability = field(converter=Reachability)
    local_system_ip: str = field(metadata={FIELD_NAME: "local-system-ip"})
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

    @property
    def is_reachable(self) -> bool:
        return self.reachability is Reachability.REACHABLE


@define(field_transformer=convert_attributes)
class Reboot(DataclassBase):
    reason: str = field(metadata={FIELD_NAME: "reboot_reason"})
    dateTime: dt.datetime = field(metadata={FIELD_NAME: "reboot_date_time"})
    vdeviceName: str = field(metadata={FIELD_NAME: "vdevice-name"})
    rebootDateTimeDate: dt.datetime = field(metadata={FIELD_NAME: "reboot_date_time-date"})
    vdeviceDataKey: str = field(metadata={FIELD_NAME: "vdevice-dataKey"})
    lastUpdated: dt.datetime = field(metadata={FIELD_NAME: "lastupdated"})
    vdeviceHostName: int = field(metadata={FIELD_NAME: "vdevice-host-name"})


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
    group: List[str]
    username: str = field(metadata={FIELD_NAME: "userName"})
    locale: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    resource_group: Optional[str] = field(default=None, metadata={FIELD_NAME: "resGroupName"})


@define
class Template(DataclassBase):
    device_type_str: str = field(metadata={FIELD_NAME: "deviceType"})
    device_type: DeviceModel = field(init=False)
    last_updated_by: str = field(metadata={FIELD_NAME: "lastUpdatedBy"})
    resource_group: str = field(metadata={FIELD_NAME: "resourceGroup"})
    template_class: str = field(metadata={FIELD_NAME: "templateClass"})
    config_type: str = field(metadata={FIELD_NAME: "configType"})
    id: str = field(metadata={FIELD_NAME: "templateId"})
    factory_default: bool = field(metadata={FIELD_NAME: "factoryDefault"})
    name: str = field(metadata={FIELD_NAME: "templateName"})
    devices_attached: int = field(metadata={FIELD_NAME: "devicesAttached"})
    description: str = field(metadata={FIELD_NAME: "templateDescription"})
    draft_mode: str = field(metadata={FIELD_NAME: "draftMode"})
    last_updated_on: dt.datetime = field(metadata={FIELD_NAME: "lastUpdatedOn"})
    template_attached: int = field(metadata={FIELD_NAME: "templateAttached"})

    def __attrs_post_init__(self):
        self.device_type = DeviceModel(self.device_type_str)


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
