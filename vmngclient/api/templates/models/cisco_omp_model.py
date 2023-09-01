from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


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

    graceful_restart: Optional[bool] = Field(True, alias="graceful-restart")
    overlay_as: Optional[int] = Field(alias="overlay-as")
    send_path_limit: Optional[int] = Field(4, alias="send-path-limit")
    ecmp_limit: Optional[int] = Field(4, alias="ecmp-limit")
    shutdown: Optional[bool]
    omp_admin_distance_ipv4: Optional[int] = Field(alias="omp-admin-distance-ipv4")
    omp_admin_distance_ipv6: Optional[int] = Field(alias="omp-admin-distance-ipv6")
    advertisement_interval: Optional[int] = Field(1, alias="advertisement-interval")
    graceful_restart_timer: Optional[int] = Field(43200, alias="graceful-restart-timer")
    eor_timer: Optional[int] = Field(300, alias="eor-timer")
    holdtime: Optional[int] = 60
    advertise: Optional[List[IPv4Advertise]]
    ipv6_advertise: Optional[List[IPv6Advertise]] = Field(alias="ipv6-advertise")
    ignore_region_path_length: Optional[bool] = Field(False, alias="ignore-region-path-length")
    transport_gateway: Optional[TransportGateway] = Field(alias="transport-gateway")
    site_types: Optional[List[SiteTypes]] = Field(alias="site-types")
    auto_translate: Optional[bool] = Field(False, alias="auto-translate")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_omp"
