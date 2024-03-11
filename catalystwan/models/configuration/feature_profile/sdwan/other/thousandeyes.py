from __future__ import annotations

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_global, as_variable

ProxyTypeStatic = Literal["static"]
ProxyTypePac = Literal["pac"]
ProxyTypeNone = Literal["none"]
TeMgmtSubnetMask = Literal[
    "255.255.255.255",
    "255.255.255.254",
    "255.255.255.252",
    "255.255.255.248",
    "255.255.255.240",
    "255.255.255.224",
    "255.255.255.192",
    "255.255.255.128",
    "255.255.255.0",
    "255.255.254.0",
    "255.255.252.0",
    "255.255.248.0",
    "255.255.240.0",
    "255.255.224.0",
    "255.255.192.0",
    "255.255.128.0",
    "255.255.0.0",
    "255.254.0.0",
    "255.252.0.0",
    "255.240.0.0",
    "255.224.0.0",
    "255.192.0.0",
    "255.128.0.0",
    "255.0.0.0",
    "254.0.0.0",
    "252.0.0.0",
    "248.0.0.0",
    "240.0.0.0",
    "224.0.0.0",
    "192.0.0.0",
    "128.0.0.0",
    "0.0.0.0",
]


class ProxyConfigStatic(BaseModel):
    """
    Web Proxy Type Config
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    proxy_type: Global[ProxyTypeStatic] = Field(
        default=as_global("static", ProxyTypeStatic),
        frozen=True,
        serialization_alias="proxyType",
        validation_alias="proxyType",
        description="Select Web Proxy Type",
    )
    proxy_host: Union[Global[str], Variable] = Field(
        default=as_variable("{{thousand_eyes_proxyconfig_proxyhost}}"),
        serialization_alias="proxyHost",
        validation_alias="proxyHost",
        description="Set the Proxy Host",
    )
    proxy_port: Union[Global[int], Variable] = Field(
        default=as_variable("{{thousand_eyes_proxyconfig_proxyport}}"),
        serialization_alias="proxyPort",
        validation_alias="proxyPort",
        description="Set the Proxy Port",
    )


class ProxyConfigPac(BaseModel):
    """
    Web Proxy Type Config
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    proxy_type: Global[ProxyTypePac] = Field(
        default=as_global("pac", ProxyTypePac),
        frozen=True,
        serialization_alias="proxyType",
        validation_alias="proxyType",
        description="Select Web Proxy Type",
    )
    pac_url: Union[Global[str], Variable] = Field(
        default=as_variable("{{thousand_eyes_proxyconfig_pacurl}}"),
        serialization_alias="pacUrl",
        validation_alias="pacUrl",
        description="Set the proxy PAC url",
    )


class ProxyConfigNone(BaseModel):
    """
    Web Proxy Type Config
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    proxy_type: Global[ProxyTypeNone] = Field(
        default=as_global("none", ProxyTypeNone),
        frozen=True,
        serialization_alias="proxyType",
        validation_alias="proxyType",
        description="Select Web Proxy Type",
    )


class VirtualApplicationItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    token: Union[Global[str], Variable] = Field(
        default=as_variable("{{thousand_eyes_token}}"), description="Set the Account Group Token"
    )
    vpn: Union[Global[int], Variable, Default[None]] = Field(
        default=Default[None](value=None), description="VPN number"
    )
    te_mgmt_ip: Optional[Union[Variable, Global[IPv4Address]]] = Field(
        default=None,
        serialization_alias="teMgmtIp",
        validation_alias="teMgmtIp",
        description="Set the Agent IP Address",
    )
    te_mgmt_subnet_mask: Optional[Union[Variable, Global[TeMgmtSubnetMask]]] = Field(
        default=None,
        serialization_alias="teMgmtSubnetMask",
        validation_alias="teMgmtSubnetMask",
        description="Set the Agent SubnetMask",
    )
    te_vpg_ip: Optional[Union[Variable, Global[IPv4Address]]] = Field(
        default=None,
        serialization_alias="teVpgIp",
        validation_alias="teVpgIp",
        description="Set the Agent default gateway",
    )
    name_server: Union[Global[IPv4Address], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="nameServer",
        validation_alias="nameServer",
        description="Set the name server",
    )
    hostname: Union[Global[str], Variable, Default[None]] = Field(
        default=Default[None](value=None), description="Set the host name"
    )
    proxy_config: Union[ProxyConfigStatic, ProxyConfigPac, ProxyConfigNone] = Field(
        default_factory=ProxyConfigNone,
        serialization_alias="proxyConfig",
        validation_alias="proxyConfig",
        description="Web Proxy Type Config",
    )


class ThousandEyesParcel(_ParcelBase):
    type_: Literal["thousandeyes"] = Field(default="thousandeyes", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    virtual_application: List[VirtualApplicationItem] = Field(
        default_factory=lambda: [VirtualApplicationItem()],
        validation_alias=AliasPath("data", "virtualApplication"),
        description="Virtual application Instance",
        max_length=1,
        min_length=1,
    )
