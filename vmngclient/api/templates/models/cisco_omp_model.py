from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel

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


class IPv4Advertise(BaseModel):
    protocol: IPv4AdvertiseProtocol
    route: Route


class IPv6AdvertiseProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    CONNECTED = "connected"
    STATIC = "static"
    EIGRP = "eigrp"
    LISP = "lisp"
    ISIS = "isis"


class IPv6Advertise(BaseModel):
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


class CiscoOMPModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    graceful_restart: Optional[bool] = Field(True, vmanage_key="graceful-restart")
    overlay_as: Optional[int] = Field(vmanage_key="overlay-as")
    send_path_limit: Optional[int] = Field(DEFAULT_OMP_SENDPATH_LIMIT, vmanage_key="send-path-limit")
    ecmp_limit: Optional[int] = Field(DEFAULT_OMP_ECMP_LIMIT, vmanage_key="ecmp-limit")
    shutdown: Optional[bool]
    omp_admin_distance_ipv4: Optional[int] = Field(vmanage_key="omp-admin-distance-ipv4")
    omp_admin_distance_ipv6: Optional[int] = Field(vmanage_key="omp-admin-distance-ipv6")
    advertisement_interval: Optional[int] = Field(
        DEFAULT_OMP_ADVERTISEMENT_INTERVAL, vmanage_key="advertisement-interval", data_path=["timers"]
    )
    graceful_restart_timer: Optional[int] = Field(
        DEFAULT_OMP_GRACEFUL_RESTART_TIMER, vmanage_key="graceful-restart-timer", data_path=["timers"]
    )
    eor_timer: Optional[int] = Field(DEFAULT_OMP_EOR_TIMER, vmanage_key="eor-timer", data_path=["timers"])
    holdtime: Optional[int] = Field(DEFAULT_OMP_HOLDTIME, data_path=["timers"])
    advertise: Optional[List[IPv4Advertise]]
    ipv6_advertise: Optional[List[IPv6Advertise]] = Field(vmanage_key="ipv6-advertise")
    ignore_region_path_length: Optional[bool] = Field(False, vmanage_key="ignore-region-path-length")
    transport_gateway: Optional[TransportGateway] = Field(vmanage_key="transport-gateway")
    site_types: Optional[List[SiteTypes]] = Field(vmanage_key="site-types")
    auto_translate: Optional[bool] = Field(False, vmanage_key="auto-translate")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_omp"
