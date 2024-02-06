from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    IkeCiphersuite,
    IkeGroup,
    IkeMode,
    IpsecCiphersuite,
    PfsGroup,
    TunnelApplication,
)


class GreAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    mask: Union[Variable, Global[str]]


class GreTunnelMode(str, Enum):
    IPv4 = "ipv4"
    IPv6 = "ipv6"


class TunnelSourceIP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tunnel_source: Union[Global[str], Variable] = Field(alias="tunnelSource")
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        alias="tunnelRouteVia", default=None
    )


class TunnelSourceIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tunnel_source_v6: Union[Global[str], Variable] = Field(alias="tunnelSourceV6")
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        alias="tunnelRouteVia", default=None
    )


class TunnelSourceInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tunnel_source_interface: Union[Global[str], Variable] = Field(alias="tunnelSourceInterface")
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        alias="tunnelRouteVia", default=None
    )


class GreSourceIp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ip: TunnelSourceIP = Field(alias="sourceIp")


class GreSourceNotLoopback(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_not_loopback: TunnelSourceInterface = Field(alias="sourceNotLoopback")


class GreSourceLoopback(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_loopback: TunnelSourceInterface = Field(alias="sourceLoopback")


class GreSourceIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ipv6: TunnelSourceIPv6 = Field(alias="sourceIpv6")


class BasicGre(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Optional[Union[Global[str], Variable]] = Field(alias="ifName", default=None)
    description: Optional[Union[Global[str], Variable, Default[None]]] = None
    address: Optional[GreAddress] = None
    ipv6_address: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="ipv6Address", default=None)
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    tunnel_protection: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="tunnelProtection", default=Default[bool](value=False)
    )
    tunnel_mode: Optional[Union[Global[GreTunnelMode], Default[GreTunnelMode]]] = Field(
        alias="tunnelMode", default=Default[GreTunnelMode](value=GreTunnelMode.IPv4)
    )
    tunnel_source_type: Optional[Union[GreSourceIp, GreSourceNotLoopback, GreSourceLoopback, GreSourceIPv6]] = Field(
        alias="tunnelSourceType", default=None
    )
    tunnel_destination: Optional[Union[Global[str], Variable]] = Field(alias="tunnelDestination", default=None)
    tunnel_destination_v6: Optional[Union[Global[str], Variable]] = Field(alias="tunnelDestinationV6", default=None)
    mtu: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=1500)
    mtu_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="mtuV6", default=None)
    tcp_mss_adjust: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="tcpMssAdjust", default=None)
    tcp_mss_adjust_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        alias="tcpMssAdjustV6", default=None
    )
    clear_dont_fragment: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="clearDontFragment", default=Default[bool](value=False)
    )
    dpd_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="dpdInterval", default=Default[int](value=10)
    )
    dpd_retries: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="dpdRetries", default=Default[int](value=3)
    )
    ike_version: Optional[Union[Global[int], Default[int]]] = Field(alias="ikeVersion", default=Default[int](value=1))
    ike_mode: Optional[Union[Global[IkeMode], Variable, Default[IkeMode]]] = Field(
        alias="ikeMode", default=Default[IkeMode](value=IkeMode.MAIN)
    )
    ike_rekey_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="ikeRekeyInterval", default=Default[int](value=14400)
    )
    ike_ciphersuite: Optional[Union[Global[IkeCiphersuite], Variable, Default[IkeCiphersuite]]] = Field(
        alias="ikeCiphersuite", default=Default[IkeCiphersuite](value=IkeCiphersuite.AES256_CBC_SHA1)
    )
    ike_group: Optional[Union[Global[IkeGroup], Variable, Default[IkeGroup]]] = Field(
        alias="ikeGroup", default=Default[IkeGroup](value=IkeGroup.GROUP_16)
    )
    pre_shared_secret: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        alias="preSharedSecret", default=None
    )
    ike_local_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="ikeLocalId", default=None)
    ike_remote_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="ikeRemoteId", default=None)
    ipsec_rekey_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="ipsecRekeyInterval", default=Default[int](value=3600)
    )
    ipsec_replay_window: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="ipsecReplayWindow", default=Default[int](value=512)
    )
    ipsec_ciphersuite: Optional[Union[Global[IpsecCiphersuite], Variable, Default[IpsecCiphersuite]]] = Field(
        alias="ipsecCiphersuite", default=Default[IpsecCiphersuite](value=IpsecCiphersuite.AES256_GCM)
    )
    perfect_forward_secrecy: Optional[Union[Global[PfsGroup], Variable, Default[PfsGroup]]] = Field(
        alias="perfectForwardSecrecy", default=Default[PfsGroup](value=PfsGroup.GROUP_16)
    )


class AdvancedGre(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    application: Optional[Union[Global[TunnelApplication], Variable]] = None


class InterfaceGreData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    basic: BasicGre
    advanced: Optional[AdvancedGre] = None


class InterfaceGreCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: InterfaceGreData
    metadata: Optional[dict] = None
