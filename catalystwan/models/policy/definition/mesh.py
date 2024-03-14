# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)


class Region(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    site_lists: List[UUID] = Field(validation_alias="siteLists", serialization_alias="siteLists")


class MeshPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vpn_list: UUID = Field(validation_alias="vpnList", serialization_alias="vpnList")
    regions: List[Region] = []


class MeshPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["mesh"] = "mesh"
    definition: MeshPolicyDefinition

    @staticmethod
    def from_vpn_list(name: str, vpn_list: UUID) -> "MeshPolicy":
        return MeshPolicy(name=name, definition=MeshPolicyDefinition(vpn_list=vpn_list))

    def add_region(self, name: str, site_lists: List[UUID]) -> Region:
        region = Region(name=name, site_lists=site_lists)
        self.definition.regions.append(region)
        return region


class MeshPolicyEditPayload(MeshPolicy, PolicyDefinitionId):
    pass


class MeshPolicyGetResponse(MeshPolicy, PolicyDefinitionGetResponse):
    pass
