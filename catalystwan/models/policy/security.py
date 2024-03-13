# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, RootModel, field_validator
from typing_extensions import Annotated

from catalystwan.models.policy.policy import (
    AdvancedInspectionProfileAssemblyItem,
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
        AdvancedMalwareProtectionAssemblyItem,
        DNSSecurityAssemblyItem,
        IntrusionPreventionAssemblyItem,
        SSLDecryptionAssemblyItem,
        URLFilteringAssemblyItem,
        ZoneBasedFWAssemblyItem,
    ],
    Field(discriminator="type"),
]

UnifiedSecurityPolicyAssemblyItem = Annotated[
    Union[
        AdvancedInspectionProfileAssemblyItem,
        DNSSecurityAssemblyItem,
        NGFirewallAssemblyItem,
    ],
    Field(discriminator="type"),
]

FailureMode = Literal[
    "open",
    "close",
]

ZoneToNoZoneInternet = Literal[
    "allow",
    "deny",
]


class HighSpeedLoggingEntry(BaseModel):
    vrf: str
    server_ip: IPvAnyAddress = Field(serialization_alias="serverIp", validation_alias="serverIp")
    port: str
    source_interface: Optional[str] = Field(serialization_alias="sourceInterface", validation_alias="sourceInterface")
    model_config = ConfigDict(populate_by_name=True)


class HighSpeedLoggingList(BaseModel):
    entries: List[HighSpeedLoggingEntry]


class LoggingEntry(BaseModel):
    vpn: str
    server_ip: IPvAnyAddress = Field(serialization_alias="serverIP", validation_alias="serverIP")
    model_config = ConfigDict(populate_by_name=True)


class SecurityPolicySettings(BaseModel):
    logging: Optional[List[LoggingEntry]] = None
    failure_mode: Optional[FailureMode] = Field(
        default=None, serialization_alias="failureMode", validation_alias="failureMode"
    )
    zone_to_no_zone_internet: ZoneToNoZoneInternet = Field(
        default="deny", serialization_alias="zoneToNozoneInternet", validation_alias="zoneToNozoneInternet"
    )
    tcp_syn_flood_limit: Optional[str] = Field(
        default=None, serialization_alias="tcpSynFloodLimit", validation_alias="tcpSynFloodLimit"
    )
    high_speed_logging: Optional[HighSpeedLoggingEntry] = Field(
        default=None, serialization_alias="highSpeedLogging", validation_alias="highSpeedLogging"
    )
    audit_trail: Optional[str] = Field(default=None, serialization_alias="auditTrail", validation_alias="auditTrail")
    platform_match: Optional[str] = Field(
        default=None, serialization_alias="platformMatch", validation_alias="platformMatch"
    )
    model_config = ConfigDict(populate_by_name=True)


class UnifiedSecurityPolicySettings(BaseModel):
    tcp_syn_flood_limit: Optional[str] = Field(
        default=None, serialization_alias="tcpSynFloodLimit", validation_alias="tcpSynFloodLimit"
    )
    max_incomplete_tcp_limit: Optional[str] = Field(
        default=None, serialization_alias="maxIncompleteTcpLimit", validation_alias="maxIncompleteTcpLimit"
    )
    max_incomplete_udp_limit: Optional[str] = Field(
        default=None, serialization_alias="maxIncompleteUdpLimit", validation_alias="maxIncompleteUdpLimit"
    )
    max_incomplete_icmp_limit: Optional[str] = Field(
        default=None, serialization_alias="maxIncompleteIcmpLimit", validation_alias="maxIncompleteIcmpLimit"
    )
    high_speed_logging: Optional[HighSpeedLoggingList] = Field(
        default=None, serialization_alias="highSpeedLogging", validation_alias="highSpeedLogging"
    )
    model_config = ConfigDict(populate_by_name=True)


class SecurityPolicyDefinition(PolicyDefinition):
    assembly: List[SecurityPolicyAssemblyItem] = []
    settings: SecurityPolicySettings = SecurityPolicySettings()


class UnifiedSecurityPolicyDefinition(PolicyDefinition):
    assembly: List[UnifiedSecurityPolicyAssemblyItem] = []
    settings: UnifiedSecurityPolicySettings = UnifiedSecurityPolicySettings()


class SecurityPolicy(PolicyCreationPayload):
    policy_mode: Union[Literal["security"], None] = Field(
        default="security", serialization_alias="policyMode", validation_alias="policyMode"
    )
    policy_type: str = Field(default="feature", serialization_alias="policyType", validation_alias="policyType")
    policy_use_case: str = Field(
        default="custom", serialization_alias="policyUseCase", validation_alias="policyUseCase"
    )
    policy_definition: SecurityPolicyDefinition = Field(
        default=SecurityPolicyDefinition(), serialization_alias="policyDefinition", validation_alias="policyDefinition"
    )

    def add_item(self, item: SecurityPolicyAssemblyItem) -> None:
        self.policy_definition.assembly.append(item)

    def add_zone_based_fw(self, definition_id: UUID) -> None:
        self.add_item(ZoneBasedFWAssemblyItem(definition_id=definition_id))

    def add_dns_security(self, definition_id: UUID) -> None:
        self.add_item(DNSSecurityAssemblyItem(definition_id=definition_id))

    def add_intrusion_prevention(self, definition_id: UUID) -> None:
        self.add_item(IntrusionPreventionAssemblyItem(definition_id=definition_id))

    def add_url_filtering(self, definition_id: UUID) -> None:
        self.add_item(URLFilteringAssemblyItem(definition_id=definition_id))

    def add_advanced_malware_protection(self, definition_id: UUID) -> None:
        self.add_item(AdvancedMalwareProtectionAssemblyItem(definition_id=definition_id))

    def add_ssl_decryption(self, definition_id: UUID) -> None:
        self.add_item(SSLDecryptionAssemblyItem(definition_id=definition_id))

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        if isinstance(policy_definition, str):
            return SecurityPolicyDefinition.model_validate_json(policy_definition)
        return policy_definition


class UnifiedSecurityPolicy(PolicyCreationPayload):
    policy_mode: Literal["unified"] = Field("unified", serialization_alias="policyMode", validation_alias="policyMode")
    policy_type: str = Field("feature", serialization_alias="policyType", validation_alias="policyType")
    policy_use_case: str = Field("custom", serialization_alias="policyUseCase", validation_alias="policyUseCase")
    policy_definition: UnifiedSecurityPolicyDefinition = Field(
        default=UnifiedSecurityPolicyDefinition(),
        serialization_alias="policyDefinition",
        validation_alias="policyDefinition",
    )

    def add_item(self, item: UnifiedSecurityPolicyAssemblyItem) -> None:
        self.policy_definition.assembly.append(item)

    def add_advanced_inspection_profile_(self, definition_id: UUID) -> None:
        self.add_item(AdvancedInspectionProfileAssemblyItem(definition_id=definition_id))

    def add_ng_firewall(self, definition_id: UUID) -> NGFirewallAssemblyItem:
        ng_fw = NGFirewallAssemblyItem(definition_id=definition_id)
        self.add_item(ng_fw)
        return ng_fw

    def add_dns_security(self, definition_id: UUID) -> None:
        self.add_item(DNSSecurityAssemblyItem(definition_id=definition_id))

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        if isinstance(policy_definition, str):
            return UnifiedSecurityPolicyDefinition.model_validate_json(policy_definition)
        return policy_definition


AnySecurityPolicy = Union[SecurityPolicy, UnifiedSecurityPolicy]


class SecurityPolicyRoot(RootModel):
    root: AnySecurityPolicy


class SecurityPolicyEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(
        default=[], serialization_alias="masterTemplatesAffected", validation_alias="masterTemplatesAffected"
    )


class SecurityPolicyInfo(SecurityPolicy, PolicyInfo):
    virtual_application_templates: List[str] = Field(
        serialization_alias="virtualApplicationTemplates", validation_alias="virtualApplicationTemplates"
    )
    supported_devices: List[str] = Field(serialization_alias="supportedDevices", validation_alias="supportedDevices")


class UnifiedSecurityPolicyInfo(UnifiedSecurityPolicy, PolicyInfo):
    virtual_application_templates: List[str] = Field(
        serialization_alias="virtualApplicationTemplates", validation_alias="virtualApplicationTemplates"
    )
    supported_devices: List[str] = Field(serialization_alias="supportedDevices", validation_alias="supportedDevices")


AnySecurityPolicyInfo = Union[SecurityPolicyInfo, UnifiedSecurityPolicyInfo]


class SecurityPolicyInfoRoot(RootModel):
    root: AnySecurityPolicyInfo
