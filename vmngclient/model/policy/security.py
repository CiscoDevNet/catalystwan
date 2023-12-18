from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, RootModel, field_validator
from typing_extensions import Annotated

from vmngclient.model.policy.policy import (
    AdvancedMalwareProtectionAssemblyItem,
    DNSSecurityAssemblyItem,
    IntrusionPreventionAssemblyItem,
    NGFirewallAssemblyItem,
    PolicyCreationPayload,
    PolicyDefinition,
    PolicyInfo,
    SSLDecryptionAssemblyItem,
    URLFilteringAssemblyItem,
    ZoneBasedFWAssemblyItem,
)

SecurityPolicyAssemblyItem = Annotated[
    Union[
        ZoneBasedFWAssemblyItem,
        IntrusionPreventionAssemblyItem,
        URLFilteringAssemblyItem,
        AdvancedMalwareProtectionAssemblyItem,
        DNSSecurityAssemblyItem,
        SSLDecryptionAssemblyItem,
    ],
    Field(discriminator="type"),
]

UnifiedSecurityPolicyAssemblyItem = Annotated[
    Union[
        NGFirewallAssemblyItem,
        DNSSecurityAssemblyItem,
    ],
    Field(discriminator="type"),
]


class FailureMode(str, Enum):
    OPEN = "open"
    CLOSE = "close"


class ZoneToNoZoneInternet(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class HighSpeedLoggingEntry(BaseModel):
    vrf: str
    server_ip: IPvAnyAddress = Field(alias="serverIp")
    port: str
    source_interface: Optional[str] = Field(alias="sourceInterface")
    model_config = ConfigDict(populate_by_name=True)


class HighSpeedLoggingList(BaseModel):
    entries: List[HighSpeedLoggingEntry]


class LoggingEntry(BaseModel):
    vpn: str
    server_ip: IPvAnyAddress = Field(alias="serverIP")
    model_config = ConfigDict(populate_by_name=True)


class SecurityPolicySettings(BaseModel):
    logging: Optional[List[LoggingEntry]] = None
    failure_mode: Optional[FailureMode] = Field(default=None, alias="failureMode")
    zone_to_no_zone_internet: ZoneToNoZoneInternet = Field(
        default=ZoneToNoZoneInternet.DENY, alias="zoneToNozoneInternet"
    )
    tcp_syn_flood_limit: Optional[str] = Field(default=None, alias="tcpSynFloodLimit")
    high_speed_logging: Optional[HighSpeedLoggingEntry] = Field(default=None, alias="highSpeedLogging")
    audit_trail: Optional[str] = Field(default=None, alias="auditTrail")
    platform_match: Optional[str] = Field(default=None, alias="platformMatch")
    model_config = ConfigDict(populate_by_name=True)


class UnifiedSecurityPolicySettings(BaseModel):
    tcp_syn_flood_limit: Optional[str] = Field(default=None, alias="tcpSynFloodLimit")
    max_incomplete_tcp_limit: Optional[str] = Field(default=None, alias="maxIncompleteTcpLimit")
    max_incomplete_udp_limit: Optional[str] = Field(default=None, alias="maxIncompleteUdpLimit")
    max_incomplete_icmp_limit: Optional[str] = Field(default=None, alias="maxIncompleteIcmpLimit")
    high_speed_logging: Optional[HighSpeedLoggingList] = Field(default=None, alias="highSpeedLogging")
    model_config = ConfigDict(populate_by_name=True)


class SecurityPolicyDefinition(PolicyDefinition):
    assembly: List[SecurityPolicyAssemblyItem] = []
    settings: SecurityPolicySettings = SecurityPolicySettings()


class UnifiedSecurityPolicyDefinition(PolicyDefinition):
    assembly: List[UnifiedSecurityPolicyAssemblyItem] = []
    settings: UnifiedSecurityPolicySettings = UnifiedSecurityPolicySettings()


class SecurityPolicy(PolicyCreationPayload):
    policy_mode: Literal["security"] = Field("security", alias="policyMode")
    policy_type: str = Field("feature", alias="policyType")
    policy_use_case: str = Field("custom", alias="policyUseCase")
    policy_definition: SecurityPolicyDefinition = Field(default=SecurityPolicyDefinition(), alias="policyDefinition")

    def add_item(self, item: SecurityPolicyAssemblyItem) -> None:
        self.policy_definition.assembly.append(item)

    def add_zone_based_fw(self, definition_id: str) -> None:
        self.add_item(ZoneBasedFWAssemblyItem(definition_id=definition_id))

    def add_dns_security(self, definition_id: str) -> None:
        self.add_item(DNSSecurityAssemblyItem(definition_id=definition_id))

    def add_intrusion_prevention(self, definition_id: str) -> None:
        self.add_item(IntrusionPreventionAssemblyItem(definition_id=definition_id))

    def add_url_filtering(self, definition_id: str) -> None:
        self.add_item(URLFilteringAssemblyItem(definition_id=definition_id))

    def add_advanced_malware_protection(self, definition_id: str) -> None:
        self.add_item(AdvancedMalwareProtectionAssemblyItem(definition_id=definition_id))

    def add_ssl_decryption(self, definition_id: str) -> None:
        self.add_item(SSLDecryptionAssemblyItem(definition_id=definition_id))

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        if isinstance(policy_definition, str):
            return SecurityPolicyDefinition.model_validate_json(policy_definition)
        return policy_definition


class UnifiedSecurityPolicy(PolicyCreationPayload):
    policy_mode: Literal["unified"] = Field("unified", alias="policyMode")
    policy_type: str = Field("feature", alias="policyType")
    policy_use_case: str = Field("custom", alias="policyUseCase")
    policy_definition: UnifiedSecurityPolicyDefinition = Field(
        default=UnifiedSecurityPolicyDefinition(), alias="policyDefinition"
    )

    def add_item(self, item: UnifiedSecurityPolicyAssemblyItem) -> None:
        self.policy_definition.assembly.append(item)

    def add_ng_firewall(self, definition_id: str) -> NGFirewallAssemblyItem:
        ng_fw = NGFirewallAssemblyItem(definition_id=definition_id)
        self.add_item(ng_fw)
        return ng_fw

    def add_dns_security(self, definition_id: str) -> None:
        self.add_item(DNSSecurityAssemblyItem(definition_id=definition_id))

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        if isinstance(policy_definition, str):
            return UnifiedSecurityPolicyDefinition.model_validate_json(policy_definition)
        return policy_definition


AnySecurityPolicy = Annotated[Union[SecurityPolicy, UnifiedSecurityPolicy], Field(discriminator="policy_mode")]


class SecurityPolicyRoot(RootModel):
    root: AnySecurityPolicy


class SecurityPolicyEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class SecurityPolicyInfo(SecurityPolicy, PolicyInfo):
    virtual_application_templates: List[str] = Field(alias="virtualApplicationTemplates")
    supported_devices: List[str] = Field(alias="supportedDevices")


class UnifiedSecurityPolicyInfo(UnifiedSecurityPolicy, PolicyInfo):
    virtual_application_templates: List[str] = Field(alias="virtualApplicationTemplates")
    supported_devices: List[str] = Field(alias="supportedDevices")


AnySecurityPolicyInfo = Annotated[
    Union[SecurityPolicyInfo, UnifiedSecurityPolicyInfo], Field(discriminator="policy_mode")
]


class SecurityPolicyInfoRoot(RootModel):
    root: AnySecurityPolicyInfo
