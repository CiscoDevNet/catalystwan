from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field, IPvAnyAddress, root_validator

from vmngclient.model.policy.policy import AssemblyItem, PolicyCreationPayload, PolicyDefinition, PolicyInfo

SecurityPolicySupportedItemTypes = Literal[
    "zoneBasedFW",
    "intrusionPrevention",
    "urlFiltering",
    "advancedMalwareProtection",
    "sslDecryption",
    "dnssecurity",
]

UnifiedSecurityPolicySupportedItemTypes = Literal[
    "zoneBasedFW",
    "dnssecurity",
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

    class Config:
        allow_population_by_field_name = True


class HighSpeedLoggingList(BaseModel):
    entries: List[HighSpeedLoggingEntry]


class LoggingEntry(BaseModel):
    vpn: str
    server_ip: IPvAnyAddress = Field(alias="serverIP")

    class Config:
        allow_population_by_field_name = True


class SecurityPolicySettings(BaseModel):
    logging: Optional[List[LoggingEntry]] = None
    failure_mode: Optional[FailureMode] = Field(None, alias="failureMode")
    zone_to_no_zone_internet: ZoneToNoZoneInternet = Field(ZoneToNoZoneInternet.DENY, alias="zoneToNozoneInternet")
    tcp_syn_flood_limit: Optional[str] = Field(None, alias="tcpSynFloodLimit")
    high_speed_logging: Optional[HighSpeedLoggingEntry] = Field(None, alias="highSpeedLogging")
    audit_trail: Optional[str] = Field(None, alias="auditTrail")
    platform_match: Optional[str] = Field(None, alias="platformMatch")

    class Config:
        allow_population_by_field_name = True


class UnifiedSecurityPolicySettings(BaseModel):
    tcp_syn_flood_limit: Optional[str] = Field(None, alias="tcpSynFloodLimit")
    max_incomplete_tcp_limit: Optional[str] = Field(None, alias="maxIncompleteTcpLimit")
    max_incomplete_udp_limit: Optional[str] = Field(None, alias="maxIncompleteUdpLimit")
    max_incomplete_icmp_limit: Optional[str] = Field(None, alias="maxIncompleteIcmpLimit")
    high_speed_logging: Optional[HighSpeedLoggingList] = Field(None, alias="highSpeedLogging")

    class Config:
        allow_population_by_field_name = True


class SecurityPolicyAssemblyItem(AssemblyItem):
    type: SecurityPolicySupportedItemTypes


class UnifiedSecurityPolicyAssemblyItem(AssemblyItem):
    type: UnifiedSecurityPolicySupportedItemTypes


class SecurityPolicyDefinition(PolicyDefinition):
    assembly: List[SecurityPolicyAssemblyItem] = []
    settings: SecurityPolicySettings = SecurityPolicySettings()  # type: ignore[call-arg]


class UnifiedSecurityPolicyDefinition(PolicyDefinition):
    assembly: List[UnifiedSecurityPolicyAssemblyItem] = []
    settings: UnifiedSecurityPolicySettings = UnifiedSecurityPolicySettings()  # type: ignore[call-arg]


class SecurityPolicy(PolicyCreationPayload):
    policy_mode: Literal["security", "unified"] = Field("security", alias="policyMode")
    policy_type: str = Field("feature", alias="policyType")
    policy_use_case: str = Field("custom", alias="policyUseCase")
    policy_definition: Union[SecurityPolicyDefinition, UnifiedSecurityPolicyDefinition] = Field(
        alias="policyDefinition"
    )

    def _add_item(self, _type: Any, item_id: str) -> None:
        if isinstance(self.policy_definition, SecurityPolicyDefinition):
            self.policy_definition.assembly.append(
                SecurityPolicyAssemblyItem(type=_type, definition_id=item_id)  # type: ignore[call-arg]
            )
        elif isinstance(self.policy_definition, UnifiedSecurityPolicyDefinition):
            self.policy_definition.assembly.append(
                UnifiedSecurityPolicyAssemblyItem(type=_type, definition_id=item_id)  # type: ignore[call-arg]
            )

    def add_zone_based_fw(self, definition_id: str) -> None:
        self._add_item("zoneBasedFW", definition_id)

    def add_intrusion_prevention(self, definition_id: str) -> None:
        self._add_item("intrusionPrevention", definition_id)

    def add_url_filtering(self, definition_id: str) -> None:
        self._add_item("urlFiltering", definition_id)

    def add_advanced_malware_protection(self, definition_id: str) -> None:
        self._add_item("advancedMalwareProtection", definition_id)

    def add_ssl_decryption(self, definition_id: str) -> None:
        self._add_item("sslDecryption", definition_id)

    @root_validator(pre=True)  # type: ignore[call-overload]
    def initialize_with_policy_mode(cls, values):
        # When instatiating model by user using constructor
        mode = values.get("policy_mode")
        definition = values.get("policy_definition")
        if definition is None:
            if mode == "unified":
                values["policy_definition"] = UnifiedSecurityPolicyDefinition()
            else:
                values["policy_definition"] = SecurityPolicyDefinition()
        return values

    @root_validator(pre=True)  # type: ignore[call-overload]
    def parse_by_policy_mode(cls, values):
        # When creating model from remote json (using aliases)
        mode = values.get("policyMode")
        definition = values.get("policyDefinition")
        if isinstance(definition, str):
            if mode == "unified":
                values["policyDefinition"] = UnifiedSecurityPolicyDefinition.parse_raw(definition)
            else:
                values["policyDefinition"] = SecurityPolicyDefinition.parse_raw(definition)
        return values

    @root_validator  # type: ignore[call-overload]
    def validate_definition(cls, values):
        mode = values.get("policy_mode")
        definition = values.get("policy_definition")
        if (mode == "security" and isinstance(definition, UnifiedSecurityPolicyDefinition)) or (
            mode == "unified" and isinstance(definition, SecurityPolicyDefinition)
        ):
            raise ValueError(f"Incompatible definition {type(definition)} for '{mode}' policy mode")
        return values


class SecurityPolicyEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class SecurityPolicyInfo(SecurityPolicy, PolicyInfo):
    virtual_application_templates: List[str] = Field(alias="virtualApplicationTemplates")
    supported_devices: List[str] = Field(alias="supportedDevices")
