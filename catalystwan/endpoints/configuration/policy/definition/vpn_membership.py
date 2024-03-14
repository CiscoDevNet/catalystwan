# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.vpn_membership import (
    VPNMembershipPolicy,
    VPNMembershipPolicyEditPayload,
    VPNMembershipPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyVPNMembershipGroupDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/vpnmembershipgroup")
    def create_policy_definition(self, payload: VPNMembershipPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/vpnmembershipgroup/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/vpnmembershipgroup/multiple/{id}
        ...

    @put("/template/policy/definition/vpnmembershipgroup/{id}")
    def edit_policy_definition(self, id: UUID, payload: VPNMembershipPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/vpnmembershipgroup", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/vpnmembershipgroup/{id}")
    def get_policy_definition(self, id: UUID) -> VPNMembershipPolicyGetResponse:
        ...

    @post("/template/policy/definition/vpnmembershipgroup/preview")
    def preview_policy_definition(self, payload: VPNMembershipPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/vpnmembershipgroup/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/vpnmembershipgroup/bulk
        ...
