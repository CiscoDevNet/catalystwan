from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator

from vmngclient.model.policy.policy import AssemblyItem, PolicyCreationPayload, PolicyDefinition, PolicyInfo

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
    flow_visibility: Optional[bool] = Field(None, alias="flowVisibility")
    flow_visibility_ipv6: Optional[bool] = Field(None, alias="flowVisibilityIPv6")
    app_visibility: Optional[bool] = Field(None, alias="appVisibility")
    app_visibility_ipv6: Optional[bool] = Field(None, alias="appVisibilityIPv6")
    cloud_qos: Optional[bool] = Field(None, alias="cloudQos")
    cloud_qos_service_side: Optional[bool] = Field(None, alias="cloudQosServiceSide")
    implicit_acl_logging: Optional[bool] = Field(None, alias="implicitAclLogging")
    log_frequency: Optional[int] = Field(None, alias="logFrequency", ge=0, le=2147483647)
    ip_visibility_cache_entries: Optional[int] = Field(None, alias="ipVisibilityCacheEntries", ge=16, le=2000000)
    ip_v6_visibility_cache_entries: Optional[int] = Field(None, alias="ipV6VisibilityCacheEntries", ge=16, le=2000000)
    model_config = ConfigDict(populate_by_name=True)


class LocalizedPolicyAssemblyItem(AssemblyItem):
    type: LocalizedPolicySupportedItemType
    definition_id: str = Field(alias="definitionId")
    model_config = ConfigDict(populate_by_name=True)


class LocalizedPolicyDefinition(PolicyDefinition):
    assembly: List[LocalizedPolicyAssemblyItem]
    settings: LocalizedPolicySettings


class LocalizedPolicy(PolicyCreationPayload):
    policy_definition: LocalizedPolicyDefinition = Field(
        default=LocalizedPolicyDefinition(assembly=[], settings=LocalizedPolicySettings()),  # type: ignore[call-arg]
        alias="policyDefinition",
    )
    policy_type: str = Field("feature", alias="policyType")

    def _add_item(self, type: LocalizedPolicySupportedItemType, id: str) -> None:
        self.policy_definition.assembly.append(
            LocalizedPolicyAssemblyItem(type=type, definition_id=id)  # type: ignore[call-arg]
        )

    def add_qos_map(self, definition_id: str) -> None:
        self._add_item("qosMap", definition_id)

    def add_rewrite_rule(self, definition_id: str) -> None:
        self._add_item("rewriteRule", definition_id)

    def add_vpn_qos_map(self, definition_id: str) -> None:
        self._add_item("vpnQoSMap", definition_id)

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
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class LocalizedPolicyDeviceInfo(BaseModel):
    local_system_ip: IPvAnyAddress = Field(alias="local-system-ip")
    host_name: str = Field(alias="host-name")
    site_id: Optional[str] = Field(None, alias="site-id")
    uuid: str
    layout_level: int = Field(alias="layoutLevel")
