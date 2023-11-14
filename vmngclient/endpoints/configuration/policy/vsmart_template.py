# mypy: disable-error-code="empty-body"
from typing import List, Optional

from pydantic.v1 import BaseModel, Field, IPvAnyAddress, validator

from vmngclient.endpoints import JSON, APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy import (
    AssemblyItem,
    PolicyCreationPayload,
    PolicyDefinition,
    PolicyEditPayload,
    PolicyId,
    PolicyInfo,
)
from vmngclient.typed_list import DataSequence


class Entry(BaseModel):
    site_lists: Optional[List[str]] = Field(alias="siteLists")
    vpn_lists: Optional[List[str]] = Field(None, alias="vpnLists")
    direction: Optional[str] = None


class VSmartAssemblyItem(AssemblyItem):
    entries: Optional[List[Entry]] = None


class VSmartPolicyDefinition(PolicyDefinition):
    assembly: List[AssemblyItem]
    region_role_assembly: List = Field(alias="regionRoleAssembly")


class VSmartTemplate(PolicyCreationPayload):
    policy_definition: VSmartPolicyDefinition = Field(alias="policyDefinition")

    @validator("policy_definition", pre=True)
    def try_parse(cls, policy_definition):
        # this is needed because GET /template/policy/vsmart contains string in policyDefinition field
        # while POST /template/policy/vsmart requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if isinstance(policy_definition, str):
            return VSmartPolicyDefinition.parse_raw(policy_definition)
        return policy_definition


class VSmartTemplateEditPayload(PolicyEditPayload, VSmartTemplate):
    rid: Optional[str] = Field(default=None, alias="@rid")
    pass


class VSmartTemplateInfo(PolicyInfo, VSmartTemplateEditPayload):
    pass


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
    def create_vsmart_template(self, payload: VSmartTemplate) -> PolicyId:
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
    def edit_template_without_lock_checks(self, id: str, payload: VSmartTemplateEditPayload) -> JSON:
        ...

    @put("/template/policy/vsmart/{id}")
    def edit_vsmart_template(self, id: str, payload: VSmartTemplateEditPayload) -> JSON:
        ...

    @get("/template/policy/vsmart", "data")
    def generate_vsmart_policy_template_list(self) -> DataSequence[VSmartTemplateInfo]:
        ...

    @get("/template/policy/vsmart/definition/{id}")
    def get_template_by_policy_id(self, id: str) -> VSmartTemplate:
        ...

    def qosmos_nbar_migration_warning(self):
        # GET /template/policy/vsmart/qosmos_nbar_migration_warning
        ...
