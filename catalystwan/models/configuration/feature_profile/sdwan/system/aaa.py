# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default, as_global


class PubkeyChainItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    key_string: Global[str] = Field(
        validation_alias="keyString",
        serialization_alias="keyString",
        pattern="^AAAA[0-9A-Za-z+/]+[=]{0,3}$",
        description="Set the RSA key string",
    )

    # Literal["ssh-rsa"]
    key_type: Global[str] = Field(
        default=Global[str](value="ssh-rsa"),
        serialization_alias="keyType",
        validation_alias="keyType",
        description="Only RSA is supported",
    )


class UserItem(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: Union[Global[str], Variable] = Field(description="Set the username")
    password: Union[Global[str], Variable] = Field(
        description=(
            "Set the user password [Note: Catalyst SD-WAN Manager will encrypt this field before saving."
            "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]"
        )
    )
    privilege: Union[Global[str], Variable, Default[str], None] = Field(
        None, description="Set Privilege Level for this user"
    )
    pubkey_chain: Optional[List[PubkeyChainItem]] = Field(
        default=None,
        validation_alias="pubkeyChain",
        serialization_alias="pubkeyChain",
        description="List of RSA public-keys per user",
        max_length=2,
    )

    def add_pubkey_chain_item(self, key: str) -> PubkeyChainItem:
        item = PubkeyChainItem(key_string=as_global(key))

        if self.pubkey_chain:
            self.pubkey_chain.append(item)
        else:
            self.pubkey_chain = [item]

        return item


class RadiusServerItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    address: Union[Global[IPv4Address], Global[IPv6Address]] = Field(description="Set IP address of Radius server")
    auth_port: Union[Global[int], Default[int], Variable, None] = Field(
        default=as_default(1812),
        validation_alias="authPort",
        serialization_alias="authPort",
        description="Set Authentication port to use to connect to Radius server",
    )
    acct_port: Union[Global[int], Default[int], Variable, None] = Field(
        default=as_default(1813),
        validation_alias="acctPort",
        serialization_alias="acctPort",
        description="Set Accounting port to use to connect to Radius server",
    )

    timeout: Union[Variable, Global[int], Default[int], None] = Field(
        default=as_default(5),
        description="Configure how long to wait for replies from the Radius server",
    )
    key: Global[str] = Field(
        description=(
            "Set the Radius server shared key [Note: Catalyst SD-WAN Manager will encrypt "
            "this field before saving. Cleartext strings will not be returned back "
            "to the user in GET responses for sensitive fields.]"
        )
    )
    secret_key: Union[Global[str], Variable, None] = Field(
        default=None,
        validation_alias="secretKey",
        serialization_alias="secretKey",
        description="Set the TACACS server shared type 7 encrypted key",
    )
    # Literal["6", "7"]
    key_enum: Union[Global[str], Default[None], None] = Field(
        default=None,
        validation_alias="keyEnum",
        serialization_alias="keyEnum",
        description="Type of encyption. To be used for type 6",
    )
    # Literal["key", "pac"]
    key_type: Union[Global[str], Default[str], Variable, None] = Field(
        default=as_default("key"), validation_alias="keyType", serialization_alias="keyType", description="key type"
    )

    retransmit: Union[Variable, Global[int], Default[int], None] = Field(
        default=as_default(3), description="Configure how many times to contact this Radius server"
    )


class Radius(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    group_name: Global[str] = Field(
        validation_alias="groupName", serialization_alias="groupName", description="Set Radius server Group Name"
    )

    vpn: Union[Global[int], Default[int], None] = Field(
        default=None, description="Set VPN in which Radius server is located"
    )
    source_interface: Union[Global[str], Default[None], Variable, None] = Field(
        default=None,
        validation_alias="sourceInterface",
        serialization_alias="sourceInterface",
        description="Set interface to use to reach Radius server",
    )
    server: List[RadiusServerItem] = Field(description="Configure the Radius server")

    @staticmethod
    def generate_radius_server(
        address: Union[IPv4Address, IPv6Address],
        key: str,
        auth_port: Optional[int] = None,
        acct_port: Optional[int] = None,
        timeout: Optional[int] = None,
        secret_key: Optional[str] = None,
        key_enum: Optional[str] = None,
        key_type: Optional[str] = None,
        retransmit: Optional[int] = None,
    ) -> RadiusServerItem:
        item = RadiusServerItem(
            address=as_global(address),
            auth_port=as_global(auth_port),
            acct_port=as_global(acct_port),
            key=as_global(key),
            retransmit=as_global(retransmit),
            timeout=as_global(timeout),
            secret_key=as_global(secret_key),
            key_enum=as_global(key_enum),
            key_type=as_global(key_type),
        )

        return item


class TacacsServerItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    address: Union[Global[IPv4Address], Global[IPv6Address]] = Field(description="Set IP address of TACACS server")
    port: Union[Variable, Global[int], Default[int], None] = Field(default=None, description="TACACS Port")
    timeout: Union[Variable, Global[int], Default[int], None] = Field(
        default=None,
        description="Configure how long to wait for replies from the TACACS server",
    )
    key: Global[str] = Field(
        description=(
            "Set the TACACS server shared key [Note: Catalyst SD-WAN Manager will encrypt"
            "this field before saving. Cleartext strings will not be returned back"
            "to the user in GET responses for sensitive fields.]"
        )
    )
    secret_key: Union[Global[str], Variable, None] = Field(
        default=None,
        validation_alias="secretKey",
        serialization_alias="secretKey",
        description="Set the TACACS server shared type 7 encrypted key",
    )
    # Literal["6", "7"]
    key_enum: Union[Global[str], Default[None], None] = Field(
        default=None,
        validation_alias="keyEnum",
        serialization_alias="keyEnum",
        description="Type of encyption. To be used for type 6",
    )


class Tacacs(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    group_name: Global[str] = Field(
        validation_alias="groupName", serialization_alias="groupName", description="Set TACACS server Group Name"
    )
    vpn: Union[Global[int], Default[int], None] = Field(
        default=None, description="Set VPN in which TACACS server is located"
    )
    source_interface: Union[Global[str], Default[str], None] = Field(
        default=None,
        validation_alias="sourceInterface",
        serialization_alias="sourceInterface",
        description="Set interface to use to reach TACACS server",
    )
    server: List[TacacsServerItem] = Field(description="Configure the TACACS server")

    @staticmethod
    def generate_tacacs_server(
        address: Union[IPv4Address, IPv6Address],
        key: str,
        port: Optional[int] = None,
        timeout: Optional[int] = None,
        secret_key: Optional[str] = None,
        key_enum: Optional[str] = None,
    ) -> TacacsServerItem:
        item = TacacsServerItem(
            address=as_global(address),
            key=as_global(key),
            port=as_global(port),
            timeout=as_global(timeout),
            secret_key=as_global(secret_key),
            key_enum=as_global(key_enum),
        )

        return item


class AccountingRuleItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    rule_id: Global[str] = Field(
        validation_alias="ruleId", serialization_alias="ruleId", description="Configure Accounting Rule ID"
    )
    # Literal['commands', 'exec', 'network', 'system']
    method: Global[str] = Field(description="Configure Accounting Method")
    # Literal['1', '15']
    level: Union[Global[str], Default[None], None] = Field(None, description="Privilege level when method is commands")
    start_stop: Union[Variable, Global[bool], Default[bool], None] = Field(
        default=None,
        validation_alias="startStop",
        serialization_alias="startStop",
        description="Record start and stop without waiting",
    )
    group: Global[List[str]] = Field(description="Use Server-group")


class AuthorizationRuleItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    rule_id: Global[str] = Field(
        validation_alias="ruleId", serialization_alias="ruleId", description="Configure Authorization Rule ID"
    )
    # Literal["commands"]
    method: Global[str]
    # Literal['1', '15']
    level: Global[str] = Field(description="Privilege level when method is commands")
    group: Global[List[str]] = Field(description="Use Server-group")
    if_authenticated: Union[Global[bool], Default[bool], None] = Field(
        default=None,
        validation_alias="ifAuthenticated",
        serialization_alias="ifAuthenticated",
        description="Succeed if user has authenticated",
    )


class AAAParcel(_ParcelBase):
    type_: Literal["aaa"] = Field(default="aaa", exclude=True)
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    authentication_group: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "authenticationGroup"),
        description="Authentication configurations parameters",
    )
    accounting_group: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "accountingGroup"),
        description="Accounting configurations parameters",
    )
    # local, radius, tacacs
    server_auth_order: Global[List[str]] = Field(
        validation_alias=AliasPath("data", "serverAuthOrder"),
        min_length=1,
        max_length=4,
        description="ServerGroups priority order",
    )
    user: Optional[List[UserItem]] = Field(
        default=None, validation_alias=AliasPath("data", "user"), description="Create local login account", min_length=1
    )
    radius: Optional[List[Radius]] = Field(
        default=None, validation_alias=AliasPath("data", "radius"), description="Configure the Radius serverGroup"
    )
    tacacs: Optional[List[Tacacs]] = Field(
        default=None, validation_alias=AliasPath("data", "tacacs"), description="Configure the TACACS serverGroup"
    )
    accounting_rule: Optional[List[AccountingRuleItem]] = Field(
        default=None, validation_alias=AliasPath("data", "accountingRule"), description="Configure the accounting rules"
    )
    authorization_console: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "authorizationConsole"),
        description="For enabling console authorization",
    )
    authorization_config_commands: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "authorizationConfigCommands"),
        description="For configuration mode commands.",
    )
    authorization_rule: Optional[List[AuthorizationRuleItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "authorizationRule"),
        description="Configure the Authorization Rules",
    )

    def add_authorization_rule(
        self, rule_id: str, method: str, level: str, group: List[str], if_authenticated: bool
    ) -> AuthorizationRuleItem:
        item = AuthorizationRuleItem(
            rule_id=as_global(rule_id),
            method=as_global(method),
            level=as_global(level),
            group=Global[List[str]](value=group),
            if_authenticated=as_global(if_authenticated),
        )

        if self.authorization_rule:
            self.authorization_rule.append(item)
        else:
            self.authorization_rule = [item]

        return item

    def add_accounting_rule(
        self, rule_id: str, method: str, level: str, group: List[str], start_stop: bool
    ) -> AccountingRuleItem:
        item = AccountingRuleItem(
            rule_id=as_global(rule_id),
            method=as_global(method),
            level=as_global(level),
            start_stop=as_global(start_stop),
            group=Global[List[str]](value=group),
        )

        if self.accounting_rule:
            self.accounting_rule.append(item)
        else:
            self.accounting_rule = [item]

        return item

    def add_radius_group(
        self, group_name: str, vpn: int, radius_servers: List[RadiusServerItem], source_interface: Optional[str] = None
    ) -> Radius:
        radius = Radius(
            group_name=as_global(group_name),
            vpn=as_global(vpn),
            server=radius_servers,
            source_interface=Default[None](value=None),
        )

        if self.radius:
            self.radius.append(radius)
        else:
            self.radius = [radius]

        return radius
