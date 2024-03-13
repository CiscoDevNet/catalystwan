# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal

from pydantic import AliasPath, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class ExpandedCommunityParcel(_ParcelBase):
    type_: Literal["expanded-community"] = Field(default="expanded-community", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    expanded_community_list: Global[list] = Field(
        default=as_global([]),
        serialization_alias="expandedCommunityList",
        validation_alias=AliasPath("data", "expandedCommunityList"),
    )

    def add_community(self, expanded_community: str):
        self.expanded_community_list.value.append(expanded_community)

    @field_validator("expanded_community_list")
    @classmethod
    def check_list_str(cls, expanded_community_list: Global):
        assert all([isinstance(ec, str) for ec in expanded_community_list.value])
        return expanded_community_list
