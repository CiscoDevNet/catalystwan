# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator

from catalystwan.models.policy.policy import AssemblyItemBase, PolicyCreationPayload, PolicyDefinition, PolicyInfo

LocalizedPolicySupportedItemType = Literal[
    "qosMap",
    "rewriteRule",
    "vpnQoSMap",
    "acl",
    "aclv6",
    "deviceaccesspolicy",
    "deviceAccessPolicy",
    "deviceaccesspolicyv6",
    "deviceAccessPolicyv6",
    "vedgeRoute",
]


class LocalizedPolicySettings(BaseModel):
    flow_visibility: Optional[bool] = Field(
        default=None, serialization_alias="flowVisibility", validation_alias="flowVisibility"
    )
    flow_visibility_ipv6: Optional[bool] = Field(
        default=None, serialization_alias="flowVisibilityIPv6", validation_alias="flowVisibilityIPv6"
    )
    app_visibility: Optional[bool] = Field(
        default=None, serialization_alias="appVisibility", validation_alias="appVisibility"
    )
    app_visibility_ipv6: Optional[bool] = Field(
        default=None, serialization_alias="appVisibilityIPv6", validation_alias="appVisibilityIPv6"
    )
    cloud_qos: Optional[bool] = Field(default=None, serialization_alias="cloudQos", validation_alias="cloudQos")
    cloud_qos_service_side: Optional[bool] = Field(
        default=None, serialization_alias="cloudQosServiceSide", validation_alias="cloudQosServiceSide"
    )
    implicit_acl_logging: Optional[bool] = Field(
        default=None, serialization_alias="implicitAclLogging", validation_alias="implicitAclLogging"
    )
    log_frequency: Optional[int] = Field(
        default=None, serialization_alias="logFrequency", validation_alias="logFrequency", ge=0, le=2147483647
    )
    ip_visibility_cache_entries: Optional[int] = Field(
        default=None,
        serialization_alias="ipVisibilityCacheEntries",
        validation_alias="ipVisibilityCacheEntries",
        ge=16,
        le=2000000,
    )
    ip_v6_visibility_cache_entries: Optional[int] = Field(
        default=None,
        serialization_alias="ipV6VisibilityCacheEntries",
        validation_alias="ipV6VisibilityCacheEntries",
        ge=16,
        le=2000000,
    )
    model_config = ConfigDict(populate_by_name=True)


class LocalizedPolicyAssemblyItem(AssemblyItemBase):
    type: LocalizedPolicySupportedItemType
    definition_id: UUID = Field(serialization_alias="definitionId", validation_alias="definitionId")
    model_config = ConfigDict(populate_by_name=True)


class LocalizedPolicyDefinition(PolicyDefinition):
    assembly: List[LocalizedPolicyAssemblyItem]
    settings: LocalizedPolicySettings


class LocalizedPolicy(PolicyCreationPayload):
    policy_definition: LocalizedPolicyDefinition = Field(
        default=LocalizedPolicyDefinition(assembly=[], settings=LocalizedPolicySettings()),
        serialization_alias="policyDefinition",
        validation_alias="policyDefinition",
    )
    policy_type: str = Field(default="feature", serialization_alias="policyType", validation_alias="policyType")

    def _add_item(self, type: LocalizedPolicySupportedItemType, id: UUID) -> None:
        self.policy_definition.assembly.append(LocalizedPolicyAssemblyItem(type=type, definition_id=id))

    def add_qos_map(self, definition_id: UUID) -> None:
        self._add_item("qosMap", definition_id)

    def add_rewrite_rule(self, definition_id: UUID) -> None:
        self._add_item("rewriteRule", definition_id)

    def add_vpn_qos_map(self, definition_id: UUID) -> None:
        self._add_item("vpnQoSMap", definition_id)

    def add_access_control_list(self, definition_id: UUID) -> None:
        self._add_item("acl", definition_id)

    def add_access_control_list_ipv6(self, definition_id: UUID) -> None:
        self._add_item("aclv6", definition_id)

    def add_device_access_policy(self, definition_id: UUID) -> None:
        self._add_item("deviceAccessPolicy", definition_id)

    def add_device_access_policy_ipv6(self, definition_id: UUID) -> None:
        self._add_item("deviceAccessPolicyv6", definition_id)

    def add_route_policy(self, definition_id: UUID) -> None:
        self._add_item("vedgeRoute", definition_id)

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        # this is needed because GET /template/policy/vedge contains string in policyDefinition field
        # while POST /template/policy/vedge requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if isinstance(policy_definition, str):
            return LocalizedPolicyDefinition.model_validate_json(policy_definition)
        return policy_definition


class LocalizedPolicyInfo(PolicyInfo, LocalizedPolicy):
    pass


class LocalizedPolicyEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(
        default=[], serialization_alias="masterTemplatesAffected", validation_alias="masterTemplatesAffected"
    )


class LocalizedPolicyDeviceInfo(BaseModel):
    local_system_ip: IPvAnyAddress = Field(serialization_alias="local-system-ip", validation_alias="local-system-ip")
    host_name: str = Field(serialization_alias="host-name", validation_alias="host-name")
    site_id: Optional[str] = Field(None, serialization_alias="site-id", validation_alias="site-id")
    uuid: UUID
    layout_level: int = Field(serialization_alias="layoutLevel", validation_alias="layoutLevel")
