from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class ExpandedCommunityListEntry(Global):
    value: List[str]


class ExpandedCommunityListData(BaseModel):
    expanded_community_list: ExpandedCommunityListEntry = Field(alias="expandedCommunityList")


class ExpandedCommunityPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.EXPANDED_COMMUNITY)
    data: ExpandedCommunityListData
