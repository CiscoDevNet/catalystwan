# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)


class Site(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    site_list: UUID = Field(validation_alias="siteList", serialization_alias="siteList")
    vpn_list: List[UUID] = Field(validation_alias="vpnList", serialization_alias="vpnList")


class VPNMembershipPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sites: List[Site] = []


class VPNMembershipPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["vpnMembershipGroup"] = "vpnMembershipGroup"
    definition: VPNMembershipPolicyDefinition = VPNMembershipPolicyDefinition()

    def add_site(self, site_list: UUID, vpn_lists: List[UUID]) -> Site:
        site = Site(site_list=site_list, vpn_list=vpn_lists)
        self.definition.sites.append(site)
        return site


class VPNMembershipPolicyEditPayload(VPNMembershipPolicy, PolicyDefinitionId):
    pass


class VPNMembershipPolicyGetResponse(VPNMembershipPolicy, PolicyDefinitionGetResponse):
    pass
