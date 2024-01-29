# mypy: disable-error-code="empty-body"
from uuid import UUID

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.models.policy.definitions.vpn_membership import VPNMembershipGroup
from vmngclient.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class VPNMembershipGroupEditPayload(VPNMembershipGroup, PolicyDefinitionId):
    pass


class VPNMembershipGroupInfo(PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class VPNMembershipGroupGetResponse(VPNMembershipGroup, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyVPNMembershipGroupDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/vpnmembershipgroup")
    def create_policy_definition(self, payload: VPNMembershipGroup) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/vpnmembershipgroup/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/vpnmembershipgroup/multiple/{id}
        ...

    @put("/template/policy/definition/vpnmembershipgroup/{id}")
    def edit_policy_definition(self, id: UUID, payload: VPNMembershipGroupEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/vpnmembershipgroup", "data")
    def get_definitions(self) -> DataSequence[VPNMembershipGroupInfo]:
        ...

    @get("/template/policy/definition/vpnmembershipgroup/{id}")
    def get_policy_definition(self, id: UUID) -> VPNMembershipGroupGetResponse:
        ...

    @post("/template/policy/definition/vpnmembershipgroup/preview")
    def preview_policy_definition(self, payload: VPNMembershipGroup) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/vpnmembershipgroup/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/vpnmembershipgroup/bulk
        ...
