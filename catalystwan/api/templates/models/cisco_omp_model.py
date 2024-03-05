# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

DEFAULT_OMP_HOLDTIME = 60
DEFAULT_OMP_EOR_TIMER = 300
DEFAULT_OMP_GRACEFUL_RESTART_TIMER = 43200
DEFAULT_OMP_ADVERTISEMENT_INTERVAL = 1
DEFAULT_OMP_SENDPATH_LIMIT = 4
DEFAULT_OMP_ECMP_LIMIT = 4


class IPv4AdvertiseProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    OSPFV3 = "ospfv3"
    CONNECTED = "connected"
    STATIC = "static"
    EIGRP = "eigrp"
    LISP = "lisp"
    ISIS = "isis"


class Route(str, Enum):
    EXTERNAL = "external"


class IPv4Advertise(FeatureTemplateValidator):
    protocol: IPv4AdvertiseProtocol
    route: Optional[Route] = None


class IPv6AdvertiseProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    CONNECTED = "connected"
    STATIC = "static"
    EIGRP = "eigrp"
    LISP = "lisp"
    ISIS = "isis"


class IPv6Advertise(FeatureTemplateValidator):
    protocol: IPv6AdvertiseProtocol


class TransportGateway(str, Enum):
    PREFER = "prefer"
    ECMP_WITH_DIRECT_PATH = "ecmp-with-direct-path"


class SiteTypes(str, Enum):
    TYPE_1 = "type-1"
    TYPE_2 = "type-2"
    TYPE_3 = "type-3"
    CLOUD = "cloud"
    BRANCH = "branch"
    BR = "br"
    SPOKE = "spoke"


class CiscoOMPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    graceful_restart: Optional[BoolStr] = Field(default=True, json_schema_extra={"vmanage_key": "graceful-restart"})
    overlay_as: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "overlay-as"})
    send_path_limit: Optional[int] = Field(
        DEFAULT_OMP_SENDPATH_LIMIT, json_schema_extra={"vmanage_key": "send-path-limit"}
    )
    ecmp_limit: Optional[int] = Field(DEFAULT_OMP_ECMP_LIMIT, json_schema_extra={"vmanage_key": "ecmp-limit"})
    shutdown: Optional[BoolStr] = None
    omp_admin_distance_ipv4: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "omp-admin-distance-ipv4"}
    )
    omp_admin_distance_ipv6: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "omp-admin-distance-ipv6"}
    )
    advertisement_interval: Optional[int] = Field(
        DEFAULT_OMP_ADVERTISEMENT_INTERVAL,
        json_schema_extra={"vmanage_key": "advertisement-interval", "data_path": ["timers"]},
    )
    graceful_restart_timer: Optional[int] = Field(
        DEFAULT_OMP_GRACEFUL_RESTART_TIMER,
        json_schema_extra={"vmanage_key": "graceful-restart-timer", "data_path": ["timers"]},
    )
    eor_timer: Optional[int] = Field(
        DEFAULT_OMP_EOR_TIMER, json_schema_extra={"vmanage_key": "eor-timer", "data_path": ["timers"]}
    )
    holdtime: Optional[int] = Field(DEFAULT_OMP_HOLDTIME, json_schema_extra={"data_path": ["timers"]})
    advertise: Optional[List[IPv4Advertise]] = None
    ipv6_advertise: Optional[List[IPv6Advertise]] = Field(
        default=None, json_schema_extra={"vmanage_key": "ipv6-advertise"}
    )
    ignore_region_path_length: Optional[BoolStr] = Field(
        default=False, json_schema_extra={"vmanage_key": "ignore-region-path-length"}
    )
    transport_gateway: Optional[TransportGateway] = Field(
        default=None, json_schema_extra={"vmanage_key": "transport-gateway"}
    )
    site_types: Optional[List[SiteTypes]] = Field(default=None, json_schema_extra={"vmanage_key": "site-types"})
    auto_translate: Optional[BoolStr] = Field(default=False, json_schema_extra={"vmanage_key": "auto-translate"})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_omp"
