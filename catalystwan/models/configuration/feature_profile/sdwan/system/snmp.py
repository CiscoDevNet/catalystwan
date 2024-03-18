from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

Authorization = Literal["read-only", "read-write"]
Priv = Literal["aes-cfb-128", "aes-256-cfb-128"]
SecurityLevel = Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]


class OidItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    id: Union[Global[str], Variable] = Field(..., description="Configure identifier of subtree of MIB objects")
    exclude: Optional[Union[Global[bool], Variable]] = Field(default=None, description="Exclude the OID")


class ViewItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Global[str] = Field(..., description="Set the name of the SNMP view")
    oid: Optional[List[OidItem]] = Field(default=None, description="Configure SNMP object identifier")


class CommunityItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Global[str] = Field(
        ...,
        description="Set name of the SNMP community"
        "[Note: Catalyst SD-WAN Manager will encrypt this field before saving."
        "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )
    user_label: Optional[Global[str]] = Field(
        default=None,
        serialization_alias="userLabel",
        validation_alias="userLabel",
        description="Set user label of the SNMP community",
    )
    view: Union[Global[str], Variable] = Field(..., description="Set name of the SNMP view")
    authorization: Optional[Union[Global[Authorization], Variable]] = Field(
        default=None, description="Configure access permissions"
    )


class GroupItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Global[str] = Field(..., description="Name of the SNMP group")
    security_level: Global[SecurityLevel] = Field(
        ...,
        serialization_alias="securityLevel",
        validation_alias="securityLevel",
        description="Configure security level",
    )
    view: Union[Global[str], Variable] = Field(..., description="Name of the SNMP view")


class UserItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Global[str] = Field(..., description="Name of the SNMP user")
    auth: Optional[Union[Global[Literal["sha"]], Variable, Default[None]]] = Field(
        default=None, description="Configure authentication protocol"
    )
    auth_password: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="authPassword",
        validation_alias="authPassword",
        description="Specify authentication protocol password",
    )
    priv: Optional[Union[Global[Priv], Variable, Default[None]]] = Field(
        default=None, description="Configure privacy protocol"
    )
    priv_password: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="privPassword",
        validation_alias="privPassword",
        description="Specify privacy protocol password",
    )
    group: Union[Global[str], Variable] = Field(..., description="Name of the SNMP group")


class TargetItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    vpn_id: Union[Global[int], Variable] = Field(
        ...,
        serialization_alias="vpnId",
        validation_alias="vpnId",
        description="Set VPN in which SNMP server is located",
    )
    ip: Union[Global[IPv4Address], Global[IPv6Address], Variable] = Field(
        ..., description="Set IPv4/IPv6 address of SNMP server"
    )
    port: Union[Global[int], Variable] = Field(..., description="Set UDP port number to connect to SNMP server")
    user_label: Optional[Global[str]] = Field(
        default=None,
        serialization_alias="userLabel",
        validation_alias="userLabel",
        description="Set user label of the SNMP community",
    )
    community_name: Optional[Union[Global[str], Variable]] = Field(
        default=None,
        serialization_alias="communityName",
        validation_alias="communityName",
        description="Set name of the SNMP community"
        "[Note: Catalyst SD-WAN Manager will encrypt this field before saving."
        "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]."
        "DEPRECATED. Use userLabel field instead",
    )
    user: Optional[Union[Global[str], Variable]] = Field(default=None, description="Set name of the SNMP user")
    source_interface: Optional[Union[Global[str], Variable]] = Field(
        default=None,
        serialization_alias="sourceInterface",
        validation_alias="sourceInterface",
        description="Source interface for outgoing SNMP traps",
    )


class SNMPParcel(_ParcelBase):
    type_: Literal["snmp"] = Field(default="snmp", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    shutdown: Union[Global[bool], Variable, Default[bool]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "shutdown"), description="Enable or disable SNMP"
    )
    contact: Union[Global[str], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "contact"),
        description="Set the contact for this managed node",
    )
    location: Union[Global[str], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "location"),
        description="Set the physical location of this managed node",
    )
    view: List[ViewItem] = Field(
        default=[], validation_alias=AliasPath("data", "view"), description="Configure a view record"
    )
    community: List[CommunityItem] = Field(
        default=[], validation_alias=AliasPath("data", "community"), description="Configure SNMP community"
    )
    group: List[GroupItem] = Field(
        default=[], validation_alias=AliasPath("data", "group"), description="Configure an SNMP group"
    )
    user: List[UserItem] = Field(
        default=[], validation_alias=AliasPath("data", "user"), description="Configure an SNMP user"
    )
    target: List[TargetItem] = Field(
        default=[],
        validation_alias=AliasPath("data", "target"),
        description="Configure SNMP server to receive SNMP traps",
    )
