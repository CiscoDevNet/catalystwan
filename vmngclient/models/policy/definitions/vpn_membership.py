from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.models.policy.policy_definition import PolicyDefinitionBase


class Site(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    site_list: UUID = Field(validation_alias="siteList", serialization_alias="siteList")
    vpn_list: List[UUID] = Field(validation_alias="vpnList", serialization_alias="vpnList")


class VPNMembershipGroupDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sites: List[Site] = []


class VPNMembershipGroup(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["vpnMembershipGroup"] = "vpnMembershipGroup"
    definition: VPNMembershipGroupDefinition = VPNMembershipGroupDefinition()

    def add_site(self, site_list: UUID, vpn_lists: List[UUID]) -> Site:
        site = Site(site_list=site_list, vpn_list=vpn_lists)
        self.definition.sites.append(site)
        return site
