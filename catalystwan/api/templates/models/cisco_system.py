from pathlib import Path
from typing import ClassVar, List, Literal, Optional
from typing_extensions import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel
from catalystwan.utils.timezone import Timezone

Epfr = Literal["disabled", "aggressive", "moderate", "conservative"]
SiteType = Literal["type-1", "type-2", "type-3", "cloud", "branch", "br", "spoke"]
ConsoleBaudRate = Literal["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
Protocol = Literal["tcp", "udp"]
Boolean = Literal["or", "and"]
Type = Literal["interface", "static-route"]
Role = Literal["edge-router", "border-router"]
EnableMrfMigration = Literal["disabled", "disabled-from-bgp-core"]


class MobileNumber(BaseModel):
    number: str


class Tracker(BaseModel):
    name: str
    endpoint_ip: Optional[str] = Field(
        default=None,
        serialization_alias="endpoint-ip",
        validation_alias="endpoint-ip",
        json_schema_extra={"vmanage_key": "endpoint-ip"},
    )
    endpoint_ip_transport_port: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "endpoint-ip", "data_path": ["endpoint-ip-transport-port"]}
    )
    protocol: Optional[Protocol] = Field(default=None, json_schema_extra={"data_path": ["endpoint-ip-transport-port"]})
    port: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["endpoint-ip-transport-port"]})
    endpoint_dns_name: Optional[str] = Field(
        default=None,
        serialization_alias="endpoint-dns-name",
        validation_alias="endpoint-dns-name",
        json_schema_extra={"vmanage_key": "endpoint-dns-name"},
    )
    endpoint_api_url: Optional[str] = Field(
        default=None,
        serialization_alias="endpoint-api-url",
        validation_alias="endpoint-api-url",
        json_schema_extra={"vmanage_key": "endpoint-api-url"},
    )
    elements: Optional[List[str]] = Field(default=None)
    boolean: Optional[Boolean] = "or"
    threshold: Optional[int] = 300
    interval: Optional[int] = 60
    multiplier: Optional[int] = 3
    type: Optional[Type] = "interface"
    model_config = ConfigDict(populate_by_name=True)


class Object(BaseModel):
    number: int


class ObjectTrack(BaseModel):
    object_number: int = Field(
        serialization_alias="object_number",
        validation_alias="object-number",
        json_schema_extra={"vmanage_key": "object-number"},
    )
    interface: str
    sig: str
    ip: str
    mask: Optional[str] = "0.0.0.0"
    vpn: int
    object: List[Object]
    boolean: Boolean
    model_config = ConfigDict(populate_by_name=True)


class AffinityPerVrf(BaseModel):
    affinity_group_number: Optional[int] = Field(
        default=None,
        serialization_alias="affinity_group_number",
        validation_alias="affinity-group-number",
        json_schema_extra={"vmanage_key": "affinity-group-number"},
    )
    vrf_range: Optional[str] = Field(
        default=None,
        serialization_alias="vrf_range",
        validation_alias="vrf-range",
        json_schema_extra={"vmanage_key": "vrf-range"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Vrf(BaseModel):
    vrf_id: int = Field(
        serialization_alias="vrf_id", validation_alias="vrf-id", json_schema_extra={"vmanage_key": "vrf-id"}
    )
    gateway_preference: Optional[List[int]] = Field(
        default=None,
        serialization_alias="gateway-preference",
        validation_alias="gateway-preference",
        json_schema_extra={"vmanage_key": "gateway-preference"},
    )
    model_config = ConfigDict(populate_by_name=True)


DeviceVariableSystemHostname = Annotated[
    DeviceVariable,
    BeforeValidator(lambda x: x if isinstance(x, DeviceVariable) else DeviceVariable(name="system_host_name")),
]
DeviceVariableSystemIp = Annotated[
    DeviceVariable, BeforeValidator(lambda x: x if isinstance(x, DeviceVariable) else DeviceVariable(name="system_ip"))
]


class CiscoSystemModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    timezone: Optional[Timezone] = Field(default=None, json_schema_extra={"data_path": ["clock"]})
    hostname: DeviceVariableSystemHostname = Field(
        default=DeviceVariable(name="system_host_name"),
        validate_default=True,
        serialization_alias="host-name",
        validation_alias="host-name",
        json_schema_extra={"vmanage_key": "host-name"},
    )
    location: Optional[str] = None
    latitude: Optional[float] = Field(default=None, json_schema_extra={"data_path": ["gps-location"]})
    longitude: Optional[float] = Field(default=None, json_schema_extra={"data_path": ["gps-location"]})
    range: Optional[int] = Field(100, json_schema_extra={"data_path": ["gps-location", "geo-fencing"]})
    enable_fencing: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["gps-location", "geo-fencing"], "vmanage_key": "enable"}
    )
    mobile_number: Optional[List[MobileNumber]] = Field(
        default=None,
        serialization_alias="mobile-number",
        validation_alias="mobile-number",
        json_schema_extra={"vmanage_key": "mobile-number", "data_path": ["gps-location", "geo-fencing", "sms"]},
    )
    enable_sms: Optional[bool] = Field(
        False, json_schema_extra={"data_path": ["gps-location", "geo-fencing", "sms"], "vmanage_key": "enable"}
    )
    device_groups: Optional[List[str]] = Field(
        default=None,
        serialization_alias="device-groups",
        validation_alias="device-groups",
        json_schema_extra={"vmanage_key": "device-groups"},
    )
    controller_group_list: Optional[List[int]] = Field(
        default=None,
        serialization_alias="controller-group-list",
        validation_alias="controller-group-list",
        json_schema_extra={"vmanage_key": "controller-group-list"},
    )
    system_ip: DeviceVariableSystemIp = Field(
        default=DeviceVariable(name="system_system_ip"),
        serialization_alias="system-ip",
        validation_alias="system-ip",
        json_schema_extra={"vmanage_key": "system-ip"},
    )
    overlay_id: Optional[int] = Field(
        default=None,
        serialization_alias="overlay-id",
        validation_alias="overlay-id",
        json_schema_extra={"vmanage_key": "overlay-id"},
    )
    site_id: int = Field(
        default=DeviceVariable(name="system_site_id"),
        serialization_alias="side-id",
        validation_alias="side-id",
        json_schema_extra={"vmanage_key": "site-id"},
    )
    site_type: Optional[List[SiteType]] = Field(
        default=None,
        validation_alias="site-type",
        serialization_alias="site-type",
        json_schema_extra={"vmanage_key": "site-type"},
    )
    port_offset: Optional[int] = Field(
        default=None,
        serialization_alias="port_offset",
        validation_alias="port_offset",
        json_schema_extra={"vmanage_key": "port-offset"},
    )
    port_hop: Optional[bool] = Field(
        default=None,
        serialization_alias="port-hop",
        validation_alias="port-hop",
        json_schema_extra={"vmanage_key": "port-hop"},
    )
    control_session_pps: Optional[int] = Field(
        default=None,
        serialization_alias="control-session-pps",
        validation_alias="control-session-pps",
        json_schema_extra={"vmanage_key": "control-session-pps"},
    )
    track_transport: Optional[bool] = Field(
        default=None,
        serialization_alias="track-transport",
        validation_alias="track-transport",
        json_schema_extra={"vmanage_key": "track-transport"},
    )
    track_interface_tag: Optional[int] = Field(
        default=None,
        validation_alias="track-interface-tag",
        serialization_alias="track-interface-tag",
        json_schema_extra={"vmanage_key": "track-interface-tag"},
    )
    console_baud_rate: Optional[ConsoleBaudRate] = Field(
        default=None,
        validation_alias="console-baud-rate",
        serialization_alias="console-baud-rate",
        json_schema_extra={"vmanage_key": "console-baud-rate"},
    )
    max_omp_sessions: Optional[int] = Field(
        default=None,
        serialization_alias="max_omp_sessions",
        validation_alias="max_omp_sessions",
        json_schema_extra={"vmanage_key": "max-omp-sessions"},
    )
    multi_tenant: Optional[bool] = Field(
        default=None,
        serialization_alias="multi-tenant",
        validation_alias="multi-tenant",
        json_schema_extra={"vmanage_key": "multi-tenant"},
    )
    track_default_gateway: Optional[bool] = Field(
        default=None,
        serialization_alias="track-default-gateway",
        validation_alias="track-default-gateway",
        json_schema_extra={"vmanage_key": "track-default-gateway"},
    )
    admin_tech_on_failure: Optional[bool] = Field(
        default=None,
        validation_alias="admin-tech-on-failure",
        serialization_alias="admin-tech-on-failure",
        json_schema_extra={"vmanage_key": "admin-tech-on-failure"},
    )
    enable_tunnel: Optional[bool] = Field(
        default=None, json_schema_extra={"vmanage_key": "enable", "data_path": ["on-demand"]}
    )
    idle_timeout: Optional[int] = Field(
        default=None,
        serialization_alias="idle-timeout",
        validation_alias="idle-timeout",
        json_schema_extra={"vmanage_key": "idle-timeout"},
    )
    on_demand_idle_timeout_min: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "idle-timeout", "data_path": ["on-demand"]}
    )
    tracker: Optional[List[Tracker]] = None
    object_track: Optional[List[ObjectTrack]] = Field(
        default=None,
        validation_alias="object-track",
        serialization_alias="object-track",
        json_schema_extra={"vmanage_key": "object-track"},
    )
    region_id: Optional[int] = Field(
        default=None,
        validation_alias="region-id",
        serialization_alias="region-id",
        json_schema_extra={"vmanage_key": "region-id"},
    )
    secondary_region: Optional[int] = Field(
        default=None,
        validation_alias="secondary-region",
        serialization_alias="secondary-region",
        json_schema_extra={"vmanage_key": "secondary-region"},
    )
    role: Optional[Role] = None
    affinity_group_number: Optional[int] = Field(
        default=None,
        validation_alias="affinity-group-number",
        serialization_alias="affinity-group-number",
        json_schema_extra={"vmanage_key": "affinity-group-number", "data_path": ["affinity-group"]},
    )
    preference: Optional[List[int]] = Field(default=None, json_schema_extra={"data_path": ["affinity-group"]})
    preference_auto: Optional[bool] = Field(
        default=None,
        validation_alias="preference-auto",
        serialization_alias="preference-auto",
        json_schema_extra={"vmanage_key": "preference-auto"},
    )
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = Field(
        default=None,
        validation_alias="affinity-per-vrf",
        serialization_alias="affinity-per-vrf",
        json_schema_extra={"vmanage_key": "affinity-per-vrf"},
    )
    transport_gateway: Optional[bool] = Field(
        default=None,
        validation_alias="transport-gateway",
        serialization_alias="transport-gateway",
        json_schema_extra={"vmanage_key": "transport-gateway"},
    )
    enable_mrf_migration: Optional[EnableMrfMigration] = Field(
        default=None,
        validation_alias="enable-mrf-migration",
        serialization_alias="enable-mrf-migration",
        json_schema_extra={"vmanage_key": "enable-mrf-migration"},
    )
    migration_bgp_community: Optional[int] = Field(
        default=None,
        validation_alias="migration-bgp-community",
        serialization_alias="migration-bgp-community",
        json_schema_extra={"vmanage_key": "migration-bgp-community"},
    )
    enable_management_region: Optional[bool] = Field(
        default=None,
        validation_alias="enable-management-region",
        serialization_alias="enable-management-region",
        json_schema_extra={"vmanage_key": "enable-management-region"},
    )
    vrf: Optional[List[Vrf]] = None
    management_gateway: Optional[bool] = Field(
        default=None,
        serialization_alias="management-gateway",
        validation_alias="management-gateway",
        json_schema_extra={"vmanage_key": "management-gateway"},
    )
    epfr: Optional[Epfr] = None

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_system"
