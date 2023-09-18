from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.device_variable import DeviceVariable
from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.timezone import Timezone


class MobileNumber(BaseModel):
    number: str


class SiteType(str, Enum):
    TYPE_1 = "type-1"
    TYPE_2 = "type-2"
    TYPE_3 = "type-3"
    CLOUD = "cloud"
    BRANCH = "branch"
    BR = "br"
    SPOKE = "spoke"


class ConsoleBaudRate(str, Enum):
    _1200 = "1200"
    _2400 = "2400"
    _4800 = "4800"
    _9600 = "9600"
    _19200 = "19200"
    _38400 = "38400"
    _57600 = "57600"
    _115200 = "115200"


class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class Boolean(str, Enum):
    OR = "or"
    AND = "and"


class Type(str, Enum):
    INTERFACE = "interface"
    STATIC_ROUTE = "static-route"


class Tracker(BaseModel):
    name: str
    endpoint_ip: str = Field(alias="endpoint-ip")
    endpoint_ip_transport_port: str = Field(alias="endpoint-ip", data_path=["endpoint-ip-transport-port"])
    protocol: Protocol = Field(data_path=["endpoint-ip-transport-port"])
    port: int = Field(data_path=["endpoint-ip-transport-port"])
    endpoint_dns_name: str = Field(alias="endpoint-dns-name")
    endpoint_api_url: str = Field(alias="endpoint-api-url")
    elements: List[str]
    boolean: Optional[Boolean] = Boolean.OR
    threshold: Optional[int] = 300
    interval: Optional[int] = 60
    multiplier: Optional[int] = 3
    type: Optional[Type] = Type.INTERFACE

    class Config:
        allow_population_by_field_name = True


class Object(BaseModel):
    number: int


class ObjectTrack(BaseModel):
    object_number: int = Field(alias="object-number")
    interface: str
    sig: str
    ip: str
    mask: Optional[str] = "0.0.0.0"
    vpn: int
    object: List[Object]
    boolean: Boolean

    class Config:
        allow_population_by_field_name = True


class Role(str, Enum):
    EDGE_ROUTER = "edge-router"
    BORDER_ROUTER = "border-router"


class AffinityPerVrf(BaseModel):
    affinity_group_number: Optional[int] = Field(alias="affinity-group-number")
    vrf_range: Optional[str] = Field(alias="vrf-range")

    class Config:
        allow_population_by_field_name = True


class EnableMrfMigration(str, Enum):
    ENABLE = "enabled"
    ENABLE_FROM_BGP_CORE = "enabled-from-bgp-core"


class Vrf(BaseModel):
    vrf_id: int = Field(alias="vrf-id")
    gateway_preference: Optional[List[int]] = Field(alias="gateway-preference")

    class Config:
        allow_population_by_field_name = True


class Epfr(str, Enum):
    DISABLED = "disabled"
    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    CONSERVATIVE = "conservative"


class CiscoSystemModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    timezone: Optional[Timezone] = Field(data_path=["clock"])
    hostname: str = Field(default=DeviceVariable(name="system_host_name"), alias="host-name", validate_default=True)
    location: Optional[str]
    latitude: Optional[float] = Field(data_path=["gps-location"])
    longitude: Optional[float] = Field(data_path=["gps-location"])
    range: Optional[int] = Field(100, data_path=["gps-location", "geo-fencing"])
    enable_fencing: Optional[bool] = Field(False, data_path=["gps-location", "geo-fencing"], alias="enable")
    mobile_number: Optional[List[MobileNumber]] = Field(
        alias="mobile-number", data_path=["gps-location", "geo-fencing", "sms"]
    )
    enable_sms: Optional[bool] = Field(False, data_path=["gps-location", "geo-fencing", "sms"], alias="enable")
    device_groups: Optional[List[str]] = Field(alias="device-groups")
    controller_group_list: Optional[List[int]] = Field(alias="controller-group-list")
    system_ip: DeviceVariable = Field(default=DeviceVariable(name="system_system_ip"), alias="system-ip")
    overlay_id: Optional[int] = Field(1, alias="overlay-id")
    site_id: int = Field(default=DeviceVariable(name="system_site_id"), alias="site-id")
    site_type: Optional[List[SiteType]] = Field(alias="site-type")
    port_offset: Optional[int] = Field(alias="port-offset")
    port_hop: Optional[bool] = Field(True, alias="port-hop")
    control_session_pps: Optional[int] = Field(300, alias="control-session-pps")
    track_transport: Optional[bool] = Field(True, alias="track-transport")
    track_interface_tag: Optional[int] = Field(alias="track-interface-tag")
    console_baud_rate: Optional[ConsoleBaudRate] = Field(alias="console-baud-rate")
    max_omp_sessions: Optional[int] = Field(alias="max-omp-sessions")
    multi_tenant: Optional[bool] = Field(alias="multi-tenant")
    track_default_gateway: Optional[bool] = Field(True, alias="track-default-gateway")
    admin_tech_on_failure: Optional[bool] = Field(alias="admin-tech-on-failure")
    enable_tunnel: Optional[bool] = Field(False, alias="enable", data_path=["on-demand"])
    idle_timeout: Optional[int] = Field(alias="idle-timeout", data_path=["on-demand"])
    tracker: Optional[List[Tracker]]
    object_track: Optional[List[ObjectTrack]] = Field(alias="object-track")
    region_id: Optional[int] = Field(alias="region-id")
    secondary_region: Optional[int] = Field(alias="secondary-region")
    role: Optional[Role]
    affinity_group_number: Optional[int] = Field(alias="affinity-group-number", data_path=["affinity-group"])
    preference: Optional[List[int]] = Field(data_path=["affinity-group"])
    preference_auto: Optional[bool] = Field(alias="preference-auto")
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = Field(alias="affinity-per-vrf")
    transport_gateway: Optional[bool] = Field(alias="transport-gateway")
    enable_mrf_migration: Optional[EnableMrfMigration] = Field(alias="enable-mrf-migration")
    migration_bgp_community: Optional[int] = Field(alias="migration-bgp-community")
    enable_management_region: Optional[bool] = Field(alias="enable-management-region")
    vrf: Optional[List[Vrf]]
    management_gateway: Optional[bool] = Field(alias="management-gateway")
    epfr: Optional[Epfr] = Epfr.DISABLED

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_system"
