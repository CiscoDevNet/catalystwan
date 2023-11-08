from typing import List, Literal, Optional

from pydantic import BaseModel, Field, validator

from vmngclient.model.policy.policy import (
    AssemblyItem,
    PolicyCreationPayload,
    PolicyDefinition,
    PolicyEditPayload,
    PolicyInfo,
)

LocalizedPolicySupportedItemType = Literal[
    "qosMap", "rewriteRule", "vpnQosMap", "acl", "aclv6", "deviceAccessPolicy", "deviceAccessPolicyv6", "vedgeRoute"
]


class LocalizedPolicySettings(BaseModel):
    flow_visibility: Optional[bool] = Field(alias="flowVisibility")
    flow_visibility_ipv6: Optional[bool] = Field(alias="flowVisibilityIPv6")
    app_visibility: Optional[bool] = Field(alias="appVisibility")
    app_visibility_ipv6: Optional[bool] = Field(alias="appVisibilityIPv6")
    cloud_qos: Optional[bool] = Field(alias="cloudQos")
    cloud_qos_service_side: Optional[bool] = Field(alias="cloudQosServiceSide")
    implicit_acl_logging: Optional[bool] = Field(alias="implicitAclLogging")
    log_frequency: Optional[int] = Field(alias="logFrequency", ge=0, le=2147483647)
    ip_visibility_cache_entries: Optional[int] = Field(alias="ipVisibilityCacheEntries", ge=16, le=2000000)
    ip_v6_visibility_cache_entries: Optional[int] = Field(alias="ipV6VisibilityCacheEntries", ge=16, le=2000000)


class LocalizedPolicyAssemblyItem(AssemblyItem):
    type: LocalizedPolicySupportedItemType
    definition_id: str = "definitionId"


class LocalizedPolicyDefinition(PolicyDefinition):
    assembly: List[LocalizedPolicyAssemblyItem]


class LocalizedPolicy(PolicyCreationPayload):
    policy_definition: LocalizedPolicyDefinition = Field(
        LocalizedPolicyDefinition(assembly=[]), alias="policyDefinition"
    )
    policy_type: str = Field("feature", const=True)

    def _add_item(self, type: LocalizedPolicySupportedItemType, id: str) -> None:
        self.policy_definition.assembly.append(LocalizedPolicyAssemblyItem(type=type, definition_id=id))

    def add_qos_map(self, definition_id: str) -> None:
        self._add_item("qosMap", definition_id)

    def add_rewrite_rule(self, definition_id: str) -> None:
        self._add_item("rewriteRule", definition_id)

    def add_vpn_qos_map(self, definition_id: str) -> None:
        self._add_item("vpnQosMap", definition_id)

    def add_access_control_list(self, definition_id: str) -> None:
        self._add_item("acl", definition_id)

    def add_access_control_list_ipv6(self, definition_id: str) -> None:
        self._add_item("aclv6", definition_id)

    def add_device_access_policy(self, definition_id: str) -> None:
        self._add_item("deviceAccessPolicy", definition_id)

    def add_device_access_policy_ipv6(self, definition_id: str) -> None:
        self._add_item("deviceAccessPolicyv6", definition_id)

    def add_route_policy(self, definition_id: str) -> None:
        self._add_item("vedgeRoute", definition_id)

    @validator("policy_definition", pre=True)
    def try_parse(cls, policy_definition):
        # this is needed because GET /template/policy/vedge contains string in policyDefinition field
        # while POST /template/policy/vedge requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if isinstance(policy_definition, str):
            return LocalizedPolicyDefinition.parse_raw(policy_definition)
        return policy_definition


class LocalizedPolicyEditPayload(PolicyEditPayload, LocalizedPolicy):
    rid: Optional[str] = Field(default=None, alias="@rid")


class LocalizedPolicyInfo(PolicyInfo, LocalizedPolicyEditPayload):
    pass
