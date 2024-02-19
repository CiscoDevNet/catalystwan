from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default


class ServerAuthOrder(str, Enum):
    LOCAL = "local"
    RADIUS = "radius"
    TACACS = "tacacs"


class User(BaseModel):
    name: Union[Global[str], Variable]
    password: Union[Global[str], Variable]
    privilege: Union[Global[str], Variable] = Field(default=as_default("15"))


class KeyString(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(..., max_length=1024, min_length=1, pattern="^AAAA[0-9A-Za-z+/]+[=]{0,3}$")


class KeyType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: Literal["ssh-rsa"]


class PubkeyChainItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key_string: KeyString = Field(..., alias="keyString", description="Set the RSA key string")
    key_type: Optional[KeyType] = Field(None, alias="keyType", description="Only RSA is supported")


# class UserItem(BaseModel):
#     model_config = ConfigDict(
#         extra='forbid',
#     )
#     name: Union[Name, Name1] = Field(..., description='Set the username')
#     password: Union[Password, Password1] = Field(
#         ...,
#         description='Set the user password [Note: Catalyst SD-WAN Manager will encrypt this field before saving. Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]',
#     )
#     privilege: Optional[Union[Privilege, Privilege1, Privilege2]] = Field(
#         None, description='Set Privilege Level for this user'
#     )
#     pubkey_chain: Optional[List[PubkeyChainItem]] = Field(
#         None,
#         alias='pubkeyChain',
#         description='List of RSA public-keys per user',
#         max_length=2,
#     )


class GroupName(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(..., max_length=32, min_length=1)


class Vpn(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=0, le=65530)


class Vpn1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=0, le=0)


class SourceInterface(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=32,
        min_length=3,
        pattern="(ATM|ATM-ACR|AppGigabitEthernet|AppNav-Compress|AppNav-UnCompress|Async|BD-VIF|BDI|CEM|CEM-ACR|Cellular|Dialer|Embedded-Service-Engine|Ethernet|Ethernet-Internal|FastEthernet|FiftyGigabitEthernet|FiveGigabitEthernet|FortyGigabitEthernet|FourHundredGigE|GMPLS|GigabitEthernet|Group-Async|HundredGigE|L2LISP|LISP|Loopback|MFR|Multilink|Port-channel|SM|Serial|Service-Engine|TenGigabitEthernet|Tunnel|TwentyFiveGigE|TwentyFiveGigabitEthernet|TwoGigabitEthernet|TwoHundredGigE|Vif|Virtual-PPP|Virtual-Template|VirtualPortGroup|Vlan|Wlan-GigabitEthernet|nat64|nat66|ntp|nve|ospfv3|overlay|pseudowire|ucse|vasileft|vasiright|vmi)([0-9]*(. ?[1-9][0-9]*)*|[0-9/]+|[0-9]+/[0-9]+/[0-9]+:[0-9]+|[0-9]+/[0-9]+/[0-9]+|[0-9]+/[0-9]+|[0-9]+)",
    )


class SourceInterface1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class SourceInterface2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")


class Address(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: Union[IPv4Address, IPv6Address]


class AuthPort(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1, le=65534)


class AuthPort1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class AuthPort2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1812, le=1812)


class AcctPort(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1, le=65534)


class AcctPort1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class AcctPort2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1813, le=1813)


class Timeout(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1, le=1000)


class Timeout1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class Timeout2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=5, le=5)


class Retransmit(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1, le=100)


class Retransmit1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class Retransmit2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=3, le=3)


class Key(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(..., min_length=1)


class SecretKey(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(..., max_length=150, min_length=1)


class SecretKey1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class SecretKey2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")


class KeyEnum(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: Literal["6", "7"]


class KeyEnum1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")


class KeyType1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: Literal["key", "pac"]


class KeyType2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class KeyType3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: Literal["key"]


class ServerItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    address: Address = Field(..., description="Set IP address of Radius server")
    auth_port: Optional[Union[AuthPort, AuthPort1, AuthPort2]] = Field(
        None,
        alias="authPort",
        description="Set Authentication port to use to connect to Radius server",
    )
    acct_port: Optional[Union[AcctPort, AcctPort1, AcctPort2]] = Field(
        None,
        alias="acctPort",
        description="Set Accounting port to use to connect to Radius server",
    )
    timeout: Optional[Union[Timeout, Timeout1, Timeout2]] = Field(
        None,
        description="Configure how long to wait for replies from the Radius server",
    )
    retransmit: Optional[Union[Retransmit, Retransmit1, Retransmit2]] = Field(
        None, description="Configure how many times to contact this Radius server"
    )
    key: Key = Field(
        ...,
        description="Set the Radius server shared key [Note: Catalyst SD-WAN Manager will encrypt this field before saving. Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )
    secret_key: Optional[Union[SecretKey, SecretKey1, SecretKey2]] = Field(
        None,
        alias="secretKey",
        description="Set the Radius server shared type 7 encrypted key",
    )
    key_enum: Optional[Union[KeyEnum, KeyEnum1]] = Field(
        None, alias="keyEnum", description="Type of encyption. To be used for type 6"
    )
    key_type: Optional[Union[KeyType1, KeyType2, KeyType3]] = Field(None, alias="keyType", description="key type")


class Radius(BaseModel):
    group_name: GroupName = Field(..., alias="groupName", description="Set Radius server Group Name")
    vpn: Optional[Union[Vpn, Vpn1]] = Field(None, description="Set VPN in which Radius server is located")
    source_interface: Optional[Union[SourceInterface, SourceInterface1, SourceInterface2]] = Field(
        None,
        alias="sourceInterface",
        description="Set interface to use to reach Radius server",
    )
    server: List[ServerItem] = Field(..., description="Configure the Radius server")


class Vpn2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=0, le=65530)


class Vpn3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=0, le=0)


class SourceInterface3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=32,
        min_length=3,
        pattern="(ATM|ATM-ACR|AppGigabitEthernet|AppNav-Compress|AppNav-UnCompress|Async|BD-VIF|BDI|CEM|CEM-ACR|Cellular|Dialer|Embedded-Service-Engine|Ethernet|Ethernet-Internal|FastEthernet|FiftyGigabitEthernet|FiveGigabitEthernet|FortyGigabitEthernet|FourHundredGigE|GMPLS|GigabitEthernet|Group-Async|HundredGigE|L2LISP|LISP|Loopback|MFR|Multilink|Port-channel|SM|Serial|Service-Engine|TenGigabitEthernet|Tunnel|TwentyFiveGigE|TwentyFiveGigabitEthernet|TwoGigabitEthernet|TwoHundredGigE|Vif|Virtual-PPP|Virtual-Template|VirtualPortGroup|Vlan|Wlan-GigabitEthernet|nat64|nat66|ntp|nve|ospfv3|overlay|pseudowire|ucse|vasileft|vasiright|vmi)([0-9]*(. ?[1-9][0-9]*)*|[0-9/]+|[0-9]+/[0-9]+/[0-9]+:[0-9]+|[0-9]+/[0-9]+/[0-9]+|[0-9]+/[0-9]+|[0-9]+)",
    )


class SourceInterface4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class SourceInterface5(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")


class Port(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1, le=65535)


class Port1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class Port2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=49, le=49)


class Timeout3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: int = Field(..., ge=1, le=1000)


class Timeout4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class Timeout5(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")
    value: int = Field(..., ge=5, le=5)


class SecretKey3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: str = Field(..., max_length=150, min_length=1)


class SecretKey4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["variable"] = Field(..., alias="optionType")
    value: str = Field(
        ...,
        max_length=64,
        min_length=1,
        pattern="^\\{\\{[.\\/\\[\\]a-zA-Z0-9_-]+\\}\\}$",
    )


class KeyEnum2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: Literal["6", "7"]


class KeyEnum3(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["default"] = Field(..., alias="optionType")


class ServerItem1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    address: Address = Field(..., description="Set IP address of TACACS server")
    port: Optional[Union[Port, Port1, Port2]] = Field(None, description="TACACS Port")
    timeout: Optional[Union[Timeout3, Timeout4, Timeout5]] = Field(
        None,
        description="Configure how long to wait for replies from the TACACS server",
    )
    key: Key = Field(
        ...,
        description="Set the TACACS server shared key [Note: Catalyst SD-WAN Manager will encrypt this field before saving. Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )
    secret_key: Optional[Union[SecretKey3, SecretKey4]] = Field(
        None,
        alias="secretKey",
        description="Set the TACACS server shared type 7 encrypted key",
    )
    key_enum: Optional[Union[KeyEnum2, KeyEnum3]] = Field(
        None, alias="keyEnum", description="Type of encyption. To be used for type 6"
    )


class Tacac(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    group_name: GroupName = Field(..., alias="groupName", description="Set TACACS server Group Name")
    vpn: Optional[Union[Vpn2, Vpn3]] = Field(None, description="Set VPN in which TACACS server is located")
    source_interface: Optional[Union[SourceInterface3, SourceInterface4, SourceInterface5]] = Field(
        None,
        alias="sourceInterface",
        description="Set interface to use to reach TACACS server",
    )
    server: List[ServerItem1] = Field(..., description="Configure the TACACS server")


class AccountingRuleItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    rule_id: Global[str] = Field(..., alias="ruleId", description="Configure Accounting Rule ID")
    # Literal['commands', 'exec', 'network', 'system']
    method: Global[str] = Field(..., description="Configure Accounting Method")
    # Literal['1', '15']
    level: Union[Global[str], Default[None], None] = Field(None, description="Privilege level when method is commands")
    start_stop: Union[Variable, Global[bool], Default[bool], None] = Field(
        None, alias="startStop", description="Record start and stop without waiting"
    )
    group: Global[List[str]] = Field(..., description="Use Server-group")


class Level2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    option_type: Literal["global"] = Field(..., alias="optionType")
    value: Literal["1", "15"]


class AuthorizationRuleItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    rule_id: Global[str] = Field(..., alias="ruleId", description="Configure Authorization Rule ID")
    method: Global[str] = Field(..., description="Method")
    # Literal['1', '15']
    level: Global[str] = Field(..., description="Privilege level when method is commands")
    group: Global[List[str]] = Field(..., description="Use Server-group")
    if_authenticated: Union[Global[bool], Default[bool], None] = Field(
        None, alias="ifAuthenticated", description="Succeed if user has authenticated"
    )


class AAA(_ParcelBase):
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
    server_auth_order: Global[List[str]] = Field(
        validation_alias=AliasPath("data", "serverAuthOrder"),
        min_length=1,
        max_length=4,
        description="ServerGroups priority order",
    )
    # TODO method
    # user: Optional[List[UserItem]] = Field(
    #     None, description='Create local login account', min_length=1
    # )
    # radius: Optional[List[Radiu]] = Field(
    #     None, description='Configure the Radius serverGroup'
    # )
    tacacs: Optional[List[Tacac]] = Field(None, description="Configure the TACACS serverGroup")
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

    # TODO add method
    authorization_rule: Optional[List[AuthorizationRuleItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "authorizationRule"),
        description="Configure the Authorization Rules",
    )
