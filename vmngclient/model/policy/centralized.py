from enum import Enum
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field, validator

from vmngclient.model.policy.policy import (
    AssemblyItem,
    PolicyCreationPayload,
    PolicyDefinition,
    PolicyEditPayload,
    PolicyInfo,
)


class TrafficDataDirectionEnum(str, Enum):
    SERVICE = "service"
    TUNNEL = "tunnel"
    ALL = "all"


class TrafficDataApplicationEntry(BaseModel):
    direction: TrafficDataDirectionEnum = TrafficDataDirectionEnum.SERVICE
    site_lists: List[str] = Field([], alias="siteLists")
    vpn_lists: List[str] = Field([], alias="vpnLists")

    class Config:
        allow_population_by_field_name = True

    def apply_site_list(self, site_list_id: str):
        self.site_lists.append(site_list_id)

    def apply_vpn_list(self, vpn_list_id: str):
        self.vpn_lists.append(vpn_list_id)


class CentralizedPolicyAssemblyItem(AssemblyItem):
    entries: Optional[List[Any]] = None


class TrafficDataApplication(CentralizedPolicyAssemblyItem):
    type: Literal["data"] = "data"
    entries: Optional[List[TrafficDataApplicationEntry]] = []


class CentralizedPolicyDefinition(PolicyDefinition):
    region_role_assembly: List = Field(default=[], alias="regionRoleAssembly")
    assembly: List[CentralizedPolicyAssemblyItem] = []

    class Config:
        allow_population_by_field_name = True


class CentralizedPolicy(PolicyCreationPayload):
    policy_definition: CentralizedPolicyDefinition = Field(alias="policyDefinition")

    def add_traffic_data(self, traffic_data_id: str) -> TrafficDataApplication:
        item = TrafficDataApplication(definition_id=traffic_data_id)  # type: ignore[call-arg]
        self.policy_definition.assembly.append(item)
        return item

    @validator("policy_definition", pre=True)
    def try_parse(cls, policy_definition):
        # this is needed because GET /template/policy/vsmart contains string in policyDefinition field
        # while POST /template/policy/vsmart requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if isinstance(policy_definition, str):
            return CentralizedPolicyDefinition.parse_raw(policy_definition)
        return policy_definition


class CentralizedPolicyEditPayload(PolicyEditPayload, CentralizedPolicy):
    rid: Optional[str] = Field(default=None, alias="@rid")


class CentralizedPolicyInfo(PolicyInfo, CentralizedPolicyEditPayload):
    pass
