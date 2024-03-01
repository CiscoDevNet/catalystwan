from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default, as_variable

IntegrityType = Literal["esp", "ip-udp-esp", "none", "ip-udp-esp-no-id"]
ReplayWindow = Literal["64", "128", "256", "512", "1024", "2048", "4096", "8192"]
DefaultReplayWindow = Literal["512"]
Tcp = Literal["aes-128-cmac", "hmac-sha-1", "hmac-sha-256"]


class KeychainItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Global[str] = Field(..., description="Specify the name of the Keychain")
    id: Global[int] = Field(..., description="Specify the Key ID")


class OneOfendChoice1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    infinite: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True), description="Infinite lifetime"
    )


class OneOfendChoice2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    duration: Union[Global[int], Variable] = Field(..., description="Send lifetime Duration (seconds)")


class OneOfendChoice3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    exact: Global[float] = Field(..., description="Configure Key lifetime end time")


class SendLifetime(BaseModel):
    """
    Send Lifetime Settings
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    local: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, description="Configure Send lifetime Local"
    )
    start_epoch: Global[float] = Field(
        ...,
        serialization_alias="startEpoch",
        validation_alias="startEpoch",
        description="Configure Key lifetime start time",
    )
    one_ofend_choice: Optional[Union[OneOfendChoice1, OneOfendChoice2, OneOfendChoice3]] = Field(
        default=None, serialization_alias="oneOfendChoice", validation_alias="oneOfendChoice"
    )


class AcceptLifetime(BaseModel):
    """
    Accept Lifetime Settings
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    local: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, description="Configure Send lifetime Local"
    )
    start_epoch: Global[float] = Field(
        ...,
        serialization_alias="startEpoch",
        validation_alias="startEpoch",
        description="Configure Key lifetime start time",
    )
    one_ofend_choice: Optional[Union[OneOfendChoice1, OneOfendChoice2, OneOfendChoice3]] = Field(
        default=None, serialization_alias="oneOfendChoice", validation_alias="oneOfendChoice"
    )


class KeyItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    id: Global[int] = Field(..., description="Select the Key ID")
    name: Global[str] = Field(..., description="Select the chain name")
    send_id: Union[Global[int], Variable] = Field(
        ..., serialization_alias="recvId", validation_alias="srecvId", description="Specify the Send ID"
    )
    recv_id: Union[Global[int], Variable] = Field(
        ..., serialization_alias="recvId", validation_alias="recvId", description="Specify the Receiver ID"
    )
    include_tcp_options: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="includeTcpOptions",
        validation_alias="includeTcpOptions",
        description="Configure Include TCP Options",
    )
    accept_ao_mismatch: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="acceptAoMismatch",
        validation_alias="acceptAoMismatch",
        description="Configure Accept AO Mismatch",
    )
    tcp: Global[Tcp] = Field(..., description="Crypto Algorithm")
    key_string: Union[Global[str], Variable] = Field(
        ...,
        serialization_alias="keyString",
        validation_alias="keyString",
        description="Specify the Key String [Note: Catalyst SD-WAN Manager will encrypt this field before saving."
        "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )
    send_lifetime: Optional[SendLifetime] = Field(
        default=None,
        serialization_alias="sendLifetime",
        validation_alias="sendLifetime",
        description="Send Lifetime Settings",
    )
    accept_lifetime: Optional[AcceptLifetime] = Field(
        default=None,
        serialization_alias="acceptLifetime",
        validation_alias="acceptLifetime",
        description="Accept Lifetime Settings",
    )


class SecurityParcel(_ParcelBase):
    type_: Literal["security"] = Field(default="security", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    rekey: Union[Global[int], Variable, Default[int]] = Field(
        default=as_default(86400),
        validation_alias=AliasPath("data", "rekey"),
        description="Set how often to change the AES key for DTLS connections",
    )
    replay_window: Optional[Union[Global[ReplayWindow], Variable, Default[DefaultReplayWindow]]] = Field(
        default=as_default("512", DefaultReplayWindow),
        validation_alias=AliasPath("data", "replayWindow"),
        description="Set the sliding replay window size",
    )
    extended_ar_window: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "extendedArWindow"),
        description="Extended Anti-Replay Window",
    )
    integrity_type: Union[Global[List[IntegrityType]], Variable] = Field(
        default=as_variable("{{security_auth_type_inte}}"),
        validation_alias=AliasPath("data", "integrityType"),
        description="Set the authentication type for DTLS connections",
    )
    pairwise_keying: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "pairwiseKeying"),
        description="Enable or disable IPsec pairwise-keying",
    )
    keychain: List[KeychainItem] = Field(
        default=[], validation_alias=AliasPath("data", "keychain"), description="Configure a Keychain"
    )
    key: List[KeyItem] = Field(default=[], validation_alias=AliasPath("data", "key"), description="Configure a Key")
