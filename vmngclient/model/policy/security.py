from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, model_validator

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


class SecurityPolicyAssemblyItem(AssemblyItem):
    type: SecurityPolicySupportedItemTypes


class UnifiedSecurityPolicyAssemblyItem(AssemblyItem):
    type: UnifiedSecurityPolicySupportedItemTypes


class SecurityPolicyDefinition(PolicyDefinition):
    assembly: List[SecurityPolicyAssemblyItem] = []
    settings: SecurityPolicySettings = SecurityPolicySettings()


class UnifiedSecurityPolicyDefinition(PolicyDefinition):
    assembly: List[UnifiedSecurityPolicyAssemblyItem] = []
    settings: UnifiedSecurityPolicySettings = UnifiedSecurityPolicySettings()


class SecurityPolicy(PolicyCreationPayload):
    policy_mode: Literal["security", "unified"] = Field("security", alias="policyMode")
    policy_type: str = Field("feature", alias="policyType")
    policy_use_case: str = Field("custom", alias="policyUseCase")
    policy_definition: Union[SecurityPolicyDefinition, UnifiedSecurityPolicyDefinition] = Field(
        default=SecurityPolicyDefinition(), alias="policyDefinition"
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

    @model_validator(mode="after")
    def initialize_with_policy_mode(self):
        # When instatiating model by user using constructor
        if self.policy_definition is None:
            if self.policy_mode == "unified":
                self.policy_definition = UnifiedSecurityPolicyDefinition()
            else:
                self.policy_definition = SecurityPolicyDefinition()
        return self

    @model_validator(mode="before")
    @classmethod
    def parse_by_policy_mode(cls, values):
        # When creating model from remote json (using aliases)
        mode = values.get("policyMode")
        definition = values.get("policyDefinition")
        if isinstance(definition, str):
            if mode == "unified":
                values["policyDefinition"] = UnifiedSecurityPolicyDefinition.model_validate_json(definition)
            else:
                values["policyDefinition"] = SecurityPolicyDefinition.model_validate_json(definition)
        if isinstance(definition, dict):
            if mode == "unified":
                values["policyDefinition"] = UnifiedSecurityPolicyDefinition.model_validate(definition)
            else:
                values["policyDefinition"] = SecurityPolicyDefinition.model_validate(definition)
        return values


class SecurityPolicyEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class SecurityPolicyInfo(SecurityPolicy, PolicyInfo):
    virtual_application_templates: List[str] = Field(alias="virtualApplicationTemplates")
    supported_devices: List[str] = Field(alias="supportedDevices")
