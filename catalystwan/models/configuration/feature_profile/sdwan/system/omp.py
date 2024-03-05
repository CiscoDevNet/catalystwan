from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

SiteTypesForTransportGateway = Literal["type-1", "type-2", "type-3", "cloud", "branch", "br", "spoke"]
TransportGateway = Literal["prefer", "ecmp-with-direct-path"]


class AdvertiseIp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    bgp: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="BGP")
    ospf: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="OSPF")
    connected: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="Variable")
    static: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="Variable")
    eigrp: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="EIGRP")
    lisp: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="LISP")
    isis: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="ISIS")


class AdvertiseIpv6(AdvertiseIp):
    pass


class AdvertiseIpv4(AdvertiseIp):
    ospfv3: Union[Variable, Global[bool], Default[bool]] = Field(default=as_default(False), description="OSPF")


class OMPParcel(_ParcelBase):
    type_: Literal["omp"] = Field(default="omp", exclude=True)

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    graceful_restart: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        validation_alias=AliasPath("data", "gracefulRestart"),
        description="Graceful Restart for OMP",
    )
    overlay_as: Union[Variable, Global[float], Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "overlayAs"),
        description="Overlay AS Number",
    )
    send_path_limit: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(4),
        validation_alias=AliasPath("data", "sendPathLimit"),
        description="Number of Paths Advertised per Prefix",
    )
    ecmp_limit: Union[Variable, Global[float], Default[int]] = Field(
        default=as_default(4),
        validation_alias=AliasPath("data", "ecmpLimit"),
        description="Set maximum number of OMP paths to install in cEdge route table",
    )
    shutdown: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "shutdown"), description="Variable"
    )
    omp_admin_distance_ipv4: Union[Variable, Global[int], Default[Optional[int]]] = Field(
        default=as_default(251),
        validation_alias=AliasPath("data", "ompAdminDistanceIpv4"),
        description="OMP Admin Distance IPv4",
    )
    omp_admin_distance_ipv6: Union[Variable, Global[int], Default[Optional[int]]] = Field(
        default=as_default(251),
        validation_alias=AliasPath("data", "ompAdminDistanceIpv6"),
        description="OMP Admin Distance IPv6",
    )
    advertisement_interval: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(1),
        validation_alias=AliasPath("data", "advertisementInterval"),
        description="Advertisement Interval (seconds)",
    )
    graceful_restart_timer: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(43200),
        validation_alias=AliasPath("data", "gracefulRestartTimer"),
        description="Graceful Restart Timer (seconds)",
    )
    eor_timer: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(300), validation_alias=AliasPath("data", "eorTimer"), description="EOR Timer"
    )
    holdtime: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(60), validation_alias=AliasPath("data", "holdtime"), description="Hold Time (seconds)"
    )
    advertise_ipv4: AdvertiseIpv4 = Field(
        default_factory=AdvertiseIpv4, validation_alias=AliasPath("data", "advertiseIpv4")
    )
    advertise_ipv6: AdvertiseIpv6 = Field(
        default_factory=AdvertiseIpv6, validation_alias=AliasPath("data", "advertiseIpv6")
    )
    ignore_region_path_length: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        None,
        validation_alias=AliasPath("data", "ignoreRegionPathLength"),
        description="Treat hierarchical and direct (secondary region) paths equally",
    )
    transport_gateway: Optional[Union[Variable, Global[TransportGateway], Default[None]]] = Field(
        None, validation_alias=AliasPath("data", "transportGateway"), description="Transport Gateway Path Behavior"
    )
    site_types_for_transport_gateway: Optional[
        Union[
            Variable,
            Global[List[SiteTypesForTransportGateway]],
            Default[None],
        ]
    ] = Field(None, validation_alias=AliasPath("data", "siteTypesForVariable"), description="Site Types")
