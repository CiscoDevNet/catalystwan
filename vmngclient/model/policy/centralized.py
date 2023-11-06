from typing import List, Optional

from pydantic import BaseModel, Field, validator

from vmngclient.model.policy.policy import (
    AssemblyItem,
    PolicyCreationPayload,
    PolicyDefinition,
    PolicyEditPayload,
    PolicyInfo,
)


class Entry(BaseModel):
    site_lists: Optional[List[str]] = Field(alias="siteLists")
    vpn_lists: Optional[List[str]] = Field(None, alias="vpnLists")
    direction: Optional[str] = None


class CentralizedPolicyAssemblyItem(AssemblyItem):
    entries: Optional[List[Entry]] = None


class CentralizedPolicyDefinition(PolicyDefinition):
    region_role_assembly: List = Field(alias="regionRoleAssembly")
    assembly: List[CentralizedPolicyAssemblyItem]


class CentralizedPolicy(PolicyCreationPayload):
    policy_definition: CentralizedPolicyDefinition = Field(alias="policyDefinition")

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
