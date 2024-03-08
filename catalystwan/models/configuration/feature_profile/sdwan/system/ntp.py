from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default


class ServerItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Union[Variable, Global[str], Global[IPv6Address], Global[IPv4Address]] = Field(
        ..., description="Set hostname or IP address of server"
    )
    key: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        None, description="Set authentication key for the server"
    )
    vpn: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(0), description="Set VPN in which NTP server is located"
    )
    version: Union[Variable, Global[int], Default[int]] = Field(default=as_default(4), description="Set NTP version")
    source_interface: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        None,
        serialization_alias="sourceInterface",
        validation_alias="sourceInterface",
        description="Set interface to use to reach NTP server",
    )
    prefer: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False), description="Variable this NTP server"
    )


class AuthenticationVariable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    key_id: Union[Variable, Global[int]] = Field(
        ..., serialization_alias="keyId", validation_alias="keyId", description="MD5 authentication key ID"
    )
    md5_value: Union[Variable, Global[str]] = Field(
        ...,
        alias="md5Value",
        description="Enter cleartext or AES-encrypted MD5 authentication key"
        "[Note: Catalyst SD-WAN Manager will encrypt this field before saving."
        "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )


class Authentication(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    authentication_keys: List[AuthenticationVariable] = Field(
        default=[],
        serialization_alias="authenticationKeys",
        validation_alias="authenticationKeys",
        description="Set MD5 authentication key",
    )
    trusted_keys: Optional[Union[Variable, Global[List[int]], Default[None]]] = Field(
        None,
        serialization_alias="trustedKeys",
        validation_alias="trustedKeys",
        description="Designate authentication key as trustworthy",
    )


class Leader(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    enable: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False), description="Variable device as NTP Leader"
    )
    stratum: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        None, description="Variable device as NTP Leader"
    )
    source: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        None, description="Variable device as NTP Leader"
    )


class NTPParcel(_ParcelBase):
    type_: Literal["ntp"] = Field(default="ntp", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    server: List[ServerItem] = Field(
        default=[], validation_alias=AliasPath("data", "server"), description="Configure NTP servers"
    )
    authentication: Authentication = Field(
        default_factory=Authentication, validation_alias=AliasPath("data", "authentication")  # type: ignore
    )
    leader: Leader = Field(default_factory=Leader, validation_alias=AliasPath("data", "leader"))  # type: ignore
