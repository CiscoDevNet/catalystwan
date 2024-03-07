# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.utils.timezone import Timezone


class MobileNumber(FeatureTemplateValidator):
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


class Tracker(FeatureTemplateValidator):
    name: str
    endpoint_ip: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "endpoint-ip"})
    endpoint_ip_transport_port: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "endpoint-ip", "data_path": ["endpoint-ip-transport-port"]}
    )
    protocol: Optional[Protocol] = Field(default=None, json_schema_extra={"data_path": ["endpoint-ip-transport-port"]})
    port: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["endpoint-ip-transport-port"]})
    endpoint_dns_name: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "endpoint-dns-name"})
    endpoint_api_url: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "endpoint-api-url"})
    elements: Optional[List[str]] = None
    boolean: Optional[Boolean] = Boolean.OR
    threshold: Optional[int] = 300
    interval: Optional[int] = 60
    multiplier: Optional[int] = 3
    type: Optional[Type] = Type.INTERFACE
    model_config = ConfigDict(populate_by_name=True)


class Object(FeatureTemplateValidator):
    number: int


class ObjectTrack(FeatureTemplateValidator):
    object_number: int = Field(json_schema_extra={"vmanage_key": "object-number"})
    interface: str
    sig: str
    ip: str
    mask: Optional[str] = "0.0.0.0"
    vpn: int
    object: List[Object]
    boolean: Boolean
    model_config = ConfigDict(populate_by_name=True)


class Role(str, Enum):
    EDGE_ROUTER = "edge-router"
    BORDER_ROUTER = "border-router"


class AffinityPerVrf(FeatureTemplateValidator):
    affinity_group_number: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "affinity-group-number"}
    )
    vrf_range: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "vrf-range"})
    model_config = ConfigDict(populate_by_name=True)


class EnableMrfMigration(str, Enum):
    ENABLE = "enabled"
    ENABLE_FROM_BGP_CORE = "enabled-from-bgp-core"


class Vrf(FeatureTemplateValidator):
    vrf_id: int = Field(json_schema_extra={"vmanage_key": "vrf-id"})
    gateway_preference: Optional[List[int]] = Field(
        default=None, json_schema_extra={"vmanage_key": "gateway-preference"}
    )
    model_config = ConfigDict(populate_by_name=True)


class Epfr(str, Enum):
    DISABLED = "disabled"
    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    CONSERVATIVE = "conservative"


class CiscoSystemModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    timezone: Optional[Timezone] = Field(default=None, json_schema_extra={"data_path": ["clock"]})
    hostname: DeviceVariable = Field(
        default=DeviceVariable(name="system_host_name"),
        validate_default=True,
        json_schema_extra={"vmanage_key": "host-name"},
    )
    location: Optional[str] = None
    latitude: Optional[float] = Field(default=None, json_schema_extra={"data_path": ["gps-location"]})
    longitude: Optional[float] = Field(default=None, json_schema_extra={"data_path": ["gps-location"]})
    range: Optional[int] = Field(100, json_schema_extra={"data_path": ["gps-location", "geo-fencing"]})
    enable_fencing: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"data_path": ["gps-location", "geo-fencing"], "vmanage_key": "enable"}
    )
    mobile_number: Optional[List[MobileNumber]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "mobile-number", "data_path": ["gps-location", "geo-fencing", "sms"]},
    )
    enable_sms: Optional[BoolStr] = Field(
        default=False, json_schema_extra={"data_path": ["gps-location", "geo-fencing", "sms"], "vmanage_key": "enable"}
    )
    device_groups: Optional[List[str]] = Field(default=None, json_schema_extra={"vmanage_key": "device-groups"})
    controller_group_list: Optional[List[int]] = Field(
        default=None, json_schema_extra={"vmanage_key": "controller-group-list"}
    )
    system_ip: DeviceVariable = Field(
        default=DeviceVariable(name="system_system_ip"), json_schema_extra={"vmanage_key": "system-ip"}
    )
    overlay_id: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "overlay-id"})
    site_id: int = Field(default=DeviceVariable(name="system_site_id"), json_schema_extra={"vmanage_key": "site-id"})
    site_type: Optional[List[SiteType]] = Field(default=None, json_schema_extra={"vmanage_key": "site-type"})
    port_offset: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "port-offset"})
    port_hop: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "port-hop"})
    control_session_pps: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "control-session-pps"})
    track_transport: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "track-transport"})
    track_interface_tag: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "track-interface-tag"})
    console_baud_rate: Optional[ConsoleBaudRate] = Field(
        default=None, json_schema_extra={"vmanage_key": "console-baud-rate"}
    )
    max_omp_sessions: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "max-omp-sessions"})
    multi_tenant: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "multi-tenant"})
    track_default_gateway: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "track-default-gateway"}
    )
    admin_tech_on_failure: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "admin-tech-on-failure"}
    )
    enable_tunnel: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "enable", "data_path": ["on-demand"]}
    )
    idle_timeout: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "idle-timeout"})
    on_demand_idle_timeout_min: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "idle-timeout", "data_path": ["on-demand"]}
    )
    tracker: Optional[List[Tracker]] = None
    object_track: Optional[List[ObjectTrack]] = Field(default=None, json_schema_extra={"vmanage_key": "object-track"})
    region_id: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "region-id"})
    secondary_region: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "secondary-region"})
    role: Optional[Role] = None
    affinity_group_number: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "affinity-group-number", "data_path": ["affinity-group"]}
    )
    preference: Optional[List[int]] = Field(default=None, json_schema_extra={"data_path": ["affinity-group"]})
    preference_auto: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "preference-auto"})
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = Field(
        default=None, json_schema_extra={"vmanage_key": "affinity-per-vrf"}
    )
    transport_gateway: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "transport-gateway"})
    enable_mrf_migration: Optional[EnableMrfMigration] = Field(
        default=None, json_schema_extra={"vmanage_key": "enable-mrf-migration"}
    )
    migration_bgp_community: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "migration-bgp-community"}
    )
    enable_management_region: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "enable-management-region"}
    )
    vrf: Optional[List[Vrf]] = None
    management_gateway: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "management-gateway"})
    epfr: Optional[Epfr] = None

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_system"
