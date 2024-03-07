# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.localized import (
    LocalizedPolicy,
    LocalizedPolicyDeviceInfo,
    LocalizedPolicyEditResponse,
    LocalizedPolicyInfo,
)
from catalystwan.models.policy.policy import PolicyId, PolicyPreview
from catalystwan.typed_list import DataSequence


class ConfigurationVEdgeTemplatePolicy(APIEndpoints):
    def change_policy_resource_group(self):
        # POST /template/policy/vedge/{resourceGroupName}/{policyId}
        ...

    @post("/template/policy/vedge")
    def create_vedge_template(self, payload: LocalizedPolicy) -> PolicyId:
        ...

    @delete("/template/policy/vedge/{id}")
    def delete_vedge_template(self, id: UUID) -> None:
        ...

    @put("/template/policy/vedge/{id}")
    def edit_vedge_template(self, id: UUID, payload: LocalizedPolicy) -> LocalizedPolicyEditResponse:
        ...

    @get("/template/policy/vedge", "data")
    def generate_policy_template_list(self) -> DataSequence[LocalizedPolicyInfo]:
        ...

    @get("/template/policy/vedge/devices/{id}", "data")
    def get_device_list_by_policy(self, id: UUID) -> DataSequence[LocalizedPolicyDeviceInfo]:
        ...

    @get("/template/policy/vedge/devices", "data")
    def get_vedge_policy_device_list(self) -> DataSequence[LocalizedPolicyDeviceInfo]:
        ...

    @get("/template/policy/vedge/definition/{id}")
    def get_vedge_template(self, id: UUID) -> LocalizedPolicy:
        ...

    @get("/template/policy/assembly/vedge/{id}")
    def preview_by_id(self, id: UUID) -> PolicyPreview:
        ...
