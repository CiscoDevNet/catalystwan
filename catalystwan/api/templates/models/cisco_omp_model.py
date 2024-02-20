import ipaddress
from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel

DEFAULT_OMP_HOLDTIME = 60
DEFAULT_OMP_EOR_TIMER = 300
DEFAULT_OMP_GRACEFUL_RESTART_TIMER = 43200
DEFAULT_OMP_ADVERTISEMENT_INTERVAL = 1
DEFAULT_OMP_SENDPATH_LIMIT = 4
DEFAULT_OMP_ECMP_LIMIT = 4

TransportGateway = Literal["prefer", "ecmp-with-direct-path"]
SiteTypes = Literal["type-1", "type-2", "type-3", "cloud", "branch", "br", "spoke"]
IPv6AdvertiseProtocol = Literal["bgp", "ospf", "connected", "static", "eigrp", "lisp", "isis"]
IPv4AdvertiseProtocol = Literal["bgp", "ospf", "ospfv3", "connected", "static", "eigrp", "lisp", "isis"]
Route = Literal["external"]


class IPv4Advertise(BaseModel):
    protocol: IPv4AdvertiseProtocol
    route: Optional[Route] = Field(default=None)


class IPv6Advertise(BaseModel):
    protocol: IPv6AdvertiseProtocol


class CiscoOMPModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    graceful_restart: Optional[bool] = Field(
        default=True,
        validation_alias="graceful-restart",
        serialization_alias="graceful-restart",
        json_schema_extra={"vmanage_key": "graceful-restart"},
    )
    overlay_as: Optional[int] = Field(
        default=None,
        validation_alias="overlay-as",
        serialization_alias="overlay-as",
        json_schema_extra={"vmanage_key": "overlay-as"},
    )
    send_path_limit: Optional[int] = Field(
        default=DEFAULT_OMP_SENDPATH_LIMIT,
        validation_alias="send-path-limit",
        serialization_alias="send-path-limit",
        json_schema_extra={"vmanage_key": "send-path-limit"},
    )
    ecmp_limit: Optional[int] = Field(
        default=DEFAULT_OMP_ECMP_LIMIT,
        validation_alias="ecmp-limit",
        serialization_alias="ecmp-limit",
        json_schema_extra={"vmanage_key": "ecmp-limit"},
    )
    shutdown: Optional[bool] = Field(default=None)
    omp_admin_distance_ipv4: Optional[int] = Field(
        default=None,
        validation_alias="omp-admin-distance-ipv4",
        serialization_alias="omp-admin-distance-ipv4",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv4"},
    )
    omp_admin_distance_ipv6: Optional[int] = Field(
        default=None,
        validation_alias="omp-admin-distance-ipv6",
        serialization_alias="omp-admin-distance-ipv6",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv6"},
    )
    advertisement_interval: Optional[int] = Field(
        DEFAULT_OMP_ADVERTISEMENT_INTERVAL,
        validation_alias="advertisement-interval",
        serialization_alias="advertisement-interval",
        json_schema_extra={"vmanage_key": "advertisement-interval", "data_path": ["timers"]},
    )
    graceful_restart_timer: Optional[int] = Field(
        DEFAULT_OMP_GRACEFUL_RESTART_TIMER,
        validation_alias="graceful-restart-timer",
        serialization_alias="graceful-restart-timer",
        json_schema_extra={"vmanage_key": "graceful-restart-timer", "data_path": ["timers"]},
    )
    eor_timer: Optional[int] = Field(
        DEFAULT_OMP_EOR_TIMER,
        validation_alias="eor-timer",
        serialization_alias="eor-timer",
        json_schema_extra={"vmanage_key": "eor-timer", "data_path": ["timers"]},
    )
    holdtime: Optional[int] = Field(default=DEFAULT_OMP_HOLDTIME, json_schema_extra={"data_path": ["timers"]})
    advertise: Optional[List[IPv4Advertise]] = Field(default=None)
    ipv6_advertise: Optional[List[IPv6Advertise]] = Field(
        default=None,
        validation_alias="ipv6-advertise",
        serialization_alias="ipv6-advertise",
        json_schema_extra={"vmanage_key": "ipv6-advertise"},
    )
    ignore_region_path_length: Optional[bool] = Field(
        False,
        validation_alias="ignore-region-path-length",
        serialization_alias="ignore-region-path-length",
        json_schema_extra={"vmanage_key": "ignore-region-path-length"},
    )
    transport_gateway: Optional[TransportGateway] = Field(
        default=None,
        validation_alias="transport-gateway",
        serialization_alias="transport-gateway",
        json_schema_extra={"vmanage_key": "transport-gateway"},
    )
    site_types: Optional[List[SiteTypes]] = Field(
        default=None,
        validation_alias="site-types",
        serialization_alias="site-types",
        json_schema_extra={"vmanage_key": "site-types"},
    )
    auto_translate: Optional[bool] = Field(
        False,
        validation_alias="auto-translate",
        serialization_alias="auto-translate",
        json_schema_extra={"vmanage_key": "auto-translate"},
    )
    dhcp_helper: Optional[List[ipaddress.IPv4Address]] = Field(
        default=None,
        serialization_alias="dhcp-helper",
        validation_alias="dhcp-helper",
        json_schema_extra={"vmanage_key": "dhcp-helper"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_omp"
