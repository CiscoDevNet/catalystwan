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


class IpsecTunnelMode(str, Enum):
    IPv4 = "ipv4"
    IPv6 = "ipv6"
    IPv4_V6_OVERLAY = "ipv4-v6overlay"


class IpsecAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    mask: Union[Variable, Global[str]]


class InterfaceIpsecData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Global[str], Variable] = Field(alias="ifName")
    shutdown: Union[Global[bool], Variable, Default[bool]] = Default[bool](value=True)
    tunnel_mode: Optional[Union[Global[IpsecTunnelMode], Default[IpsecTunnelMode]]] = Field(
        alias="tunnelMode", default=Default[IpsecTunnelMode](value=IpsecTunnelMode.IPv4)
    )
    description: Union[Global[str], Variable, Default[None]] = Default[None](value=None)
    address: Optional[IpsecAddress] = None
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(alias="ipv6Address", default=None)
    tunnel_source: Optional[IpsecAddress] = Field(alias="tunnelSource", default=None)
    tunnel_source_v6: Optional[Union[Global[str], Variable]] = Field(alias="tunnelSourceV6", default=None)
    tunnel_source_interface: Optional[Union[Global[str], Variable]] = Field(alias="tunnelSourceInterface", default=None)
    tunnel_destination: Optional[IpsecAddress] = Field(alias="tunnelDestination", default=None)
    tunnel_destination_v6: Optional[Union[Global[str], Variable]] = Field(alias="tunnelDestinationV6", default=None)
    application: Union[Global[TunnelApplication], Variable]
    tcp_mss_adjust: Union[Global[int], Variable, Default[None]] = Field(
        alias="tcpMssAdjust", default=Default[None](value=None)
    )
    tcp_mss_adjust_v6: Union[Global[int], Variable, Default[None]] = Field(
        alias="tcpMssAdjustV6", default=Default[None](value=None)
    )
    clear_dont_fragment: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="clearDontFragment", default=Default[bool](value=False)
    )
    mtu: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=1500)
    mtu_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="mtuV6", default=None)
    dpd_interval: Union[Global[int], Variable, Default[int]] = Field(
        alias="dpdInterval", default=Default[int](value=10)
    )
    dpd_retries: Union[Global[int], Variable, Default[int]] = Field(alias="dpdRetries", default=Default[int](value=3))
    ike_version: Union[Global[int], Default[int]] = Field(alias="ikeVersion", default=Default[int](value=1))
    ike_mode: Optional[Union[Global[IkeMode], Variable, Default[IkeMode]]] = Field(
        alias="ikeMode", default=Default[IkeMode](value=IkeMode.MAIN)
    )
    ike_rekey_interval: Union[Global[int], Variable, Default[int]] = Field(
        alias="ikeRekeyInterval", default=Default[int](value=14400)
    )
    ike_ciphersuite: Union[Global[IkeCiphersuite], Variable, Default[IkeCiphersuite]] = Field(
        alias="ikeCiphersuite", default=Default[IkeCiphersuite](value=IkeCiphersuite.AES256_CBC_SHA1)
    )
    ike_group: Union[Global[IkeGroup], Variable, Default[IkeGroup]] = Field(
        alias="ikeGroup", default=Default[IkeGroup](value=IkeGroup.GROUP_16)
    )
    pre_shared_secret: Union[Global[str], Variable] = Field(alias="preSharedSecret")
    ike_local_id: Union[Global[str], Variable, Default[None]] = Field(alias="ikeLocalId")
    ike_remote_id: Union[Global[str], Variable, Default[None]] = Field(alias="ikeRemoteId")
    ipsec_rekey_interval: Union[Global[int], Variable, Default[int]] = Field(
        alias="ipsecRekeyInterval", default=Default[int](value=3600)
    )
    ipsec_replay_window: Union[Global[int], Variable, Default[int]] = Field(
        alias="ipsecReplayWindow", default=Default[int](value=512)
    )
    ipsec_ciphersuite: Union[Global[IpsecCiphersuite], Variable, Default[IpsecCiphersuite]] = Field(
        alias="ipsecCiphersuite", default=Default[IpsecCiphersuite](value=IpsecCiphersuite.AES256_GCM)
    )
    perfect_forward_secrecy: Union[Global[PfsGroup], Variable, Default[PfsGroup]] = Field(
        alias="perfectForwardSecrecy", default=Default[PfsGroup](value=PfsGroup.GROUP_16)
    )
    tracker: Optional[Union[Global[str], Variable, Default[None]]] = None
    tunnel_route_via: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        alias="tunnelRouteVia", default=None
    )


class InterfaceIpsecCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: InterfaceIpsecData
