from enum import Enum
from typing import Any, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from vmngclient.models.policy.policy import (
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
    site_lists: List[UUID] = Field([], serialization_alias="siteLists", validation_alias="siteLists")
    vpn_lists: List[UUID] = Field([], serialization_alias="vpnLists", validation_alias="vpnLists")
    model_config = ConfigDict(populate_by_name=True)

    def apply_site_list(self, site_list_id: UUID):
        self.site_lists.append(site_list_id)

    def apply_vpn_list(self, vpn_list_id: UUID):
        self.vpn_lists.append(vpn_list_id)


class CentralizedPolicyAssemblyItem(AssemblyItem):
    entries: Optional[List[Any]] = None


class TrafficDataApplication(CentralizedPolicyAssemblyItem):
    type: Literal["data"] = "data"
    entries: List[TrafficDataApplicationEntry] = []

    def apply(
        self,
        site_list_ids: List[UUID],
        vpn_list_ids: List[UUID],
        direction: TrafficDataDirectionEnum = TrafficDataDirectionEnum.SERVICE,
    ) -> None:
        entry = TrafficDataApplicationEntry(
            direction=direction,
            site_lists=site_list_ids,
            vpn_lists=vpn_list_ids,
        )
        self.entries.append(entry)


class CentralizedPolicyDefinition(PolicyDefinition):
    region_role_assembly: List = Field(
        default=[], serialization_alias="regionRoleAssembly", validation_alias="regionRoleAssembly"
    )
    assembly: List[CentralizedPolicyAssemblyItem] = []
    model_config = ConfigDict(populate_by_name=True)


class CentralizedPolicy(PolicyCreationPayload):
    policy_definition: CentralizedPolicyDefinition = Field(
        CentralizedPolicyDefinition(), serialization_alias="policyDefinition", validation_alias="policyDefinition"
    )
    policy_type: str = Field("feature", serialization_alias="policyType", validation_alias="policyType")

    def add_traffic_data_policy(self, traffic_data_id: UUID) -> TrafficDataApplication:
        item = TrafficDataApplication(definition_id=traffic_data_id)
        self.policy_definition.assembly.append(item)
        return item

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        # this is needed because GET /template/policy/vsmart contains string in policyDefinition field
        # while POST /template/policy/vsmart requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if isinstance(policy_definition, str):
            return CentralizedPolicyDefinition.parse_raw(policy_definition)
        return policy_definition


class CentralizedPolicyEditPayload(PolicyEditPayload, CentralizedPolicy):
    rid: Optional[str] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")


class CentralizedPolicyInfo(PolicyInfo, CentralizedPolicyEditPayload):
    pass
