from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class ExpandedCommunityListData(BaseModel):
    expanded_community_list: Global[str] = Field(
        serialization_alias="expandedCommunityList", validation_alias="expandedCommunityList"
    )


class ExpandedCommunityParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.EXPANDED_COMMUNITY)
    data: ExpandedCommunityListData
