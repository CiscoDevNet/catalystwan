# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.localized import (
    LocalizedPolicy,
    LocalizedPolicyDeviceInfo,
    LocalizedPolicyEditResponse,
    LocalizedPolicyInfo,
)
from vmngclient.model.policy.policy import PolicyId, PolicyPreview
from vmngclient.typed_list import DataSequence


class ConfigurationVEdgeTemplatePolicy(APIEndpoints):
    def change_policy_resource_group(self):
        # POST /template/policy/vedge/{resourceGroupName}/{policyId}
        ...

    @post("/template/policy/vedge")
    def create_vedge_template(self, payload: LocalizedPolicy) -> PolicyId:
        ...

    @delete("/template/policy/vedge/{id}")
    def delete_vedge_template(self, id: str) -> None:
        ...

    @put("/template/policy/vedge/{id}")
    def edit_vedge_template(self, id: str, payload: LocalizedPolicy) -> LocalizedPolicyEditResponse:
        ...

    @get("/template/policy/vedge", "data")
    def generate_policy_template_list(self) -> DataSequence[LocalizedPolicyInfo]:
        ...

    @get("/template/policy/vedge/devices/{id}", "data")
    def get_device_list_by_policy(self, id: str) -> DataSequence[LocalizedPolicyDeviceInfo]:
        ...

    @get("/template/policy/vedge/devices", "data")
    def get_vedge_policy_device_list(self) -> DataSequence[LocalizedPolicyDeviceInfo]:
        ...

    @get("/template/policy/vedge/definition/{id}")
    def get_vedge_template(self, id: str) -> LocalizedPolicy:
        ...

    @get("/template/policy/assembly/vedge/{id}")
    def preview_by_id(self, id: str) -> PolicyPreview:
        ...
