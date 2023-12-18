# mypy: disable-error-code="empty-body"

from pydantic.v1 import BaseModel, Field, IPvAnyAddress

from vmngclient.endpoints import JSON, APIEndpoints, delete, get, post, put
from vmngclient.model.policy.centralized import CentralizedPolicy, CentralizedPolicyEditPayload, CentralizedPolicyInfo
from vmngclient.model.policy.policy import PolicyId
from vmngclient.typed_list import DataSequence


class VSmartConnectivityStatus(BaseModel):
    device_uuid: str = Field(alias="deviceUUID")
    operation_mode: str = Field(alias="operationMode")
    device_ip: IPvAnyAddress = Field(alias="deviceIp")
    local_system_ip: IPvAnyAddress = Field(alias="local-system-ip")
    is_online: bool = Field(alias="isOnline")


class AutoConfirm(BaseModel):
    confirm: str = Field(default="true", const=True)


class ActivateDeactivateTaskId(BaseModel):
    id: str


class ConfigurationVSmartTemplatePolicy(APIEndpoints):
    @post("/template/policy/vsmart/activate/{id}")
    def activate_policy(
        self, id: str, params: AutoConfirm = AutoConfirm(), payload: JSON = {}
    ) -> ActivateDeactivateTaskId:
        ...

    def activate_policy_for_cloud_services(self):
        # POST /template/policy/vsmart/activate/central/{policyId}
        ...

    @get("/template/policy/vsmart/connectivity/status", "data")
    def check_vsmart_connectivity_status(self) -> DataSequence[VSmartConnectivityStatus]:
        ...

    @post("/template/policy/vsmart")
    def create_vsmart_template(self, payload: CentralizedPolicy) -> PolicyId:
        ...

    @post("/template/policy/vsmart/deactivate/{id}")
    def deactivate_policy(
        self, id: str, params: AutoConfirm = AutoConfirm(), payload: JSON = {}
    ) -> ActivateDeactivateTaskId:
        ...

    @delete("/template/policy/vsmart/{id}")
    def delete_vsmart_template(self, id: str) -> None:
        ...

    @put("/template/policy/vsmart/central/{id}")
    def edit_template_without_lock_checks(self, id: str, payload: CentralizedPolicyEditPayload) -> JSON:
        ...

    @put("/template/policy/vsmart/{id}")
    def edit_vsmart_template(self, id: str, payload: CentralizedPolicyEditPayload) -> JSON:
        ...

    @get("/template/policy/vsmart", "data")
    def generate_vsmart_policy_template_list(self) -> DataSequence[CentralizedPolicyInfo]:
        ...

    @get("/template/policy/vsmart/definition/{id}")
    def get_template_by_policy_id(self, id: str) -> CentralizedPolicy:
        ...

    def qosmos_nbar_migration_warning(self):
        # GET /template/policy/vsmart/qosmos_nbar_migration_warning
        ...
