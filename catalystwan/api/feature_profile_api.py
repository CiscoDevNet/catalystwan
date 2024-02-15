from __future__ import annotations

from typing import TYPE_CHECKING, Protocol
from uuid import UUID

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.api.parcel_api import SDRoutingFullConfigParcelAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.policy_object import PolicyObjectFeatureProfile
from catalystwan.endpoints.configuration_feature_profile import SDRoutingConfigurationFeatureProfile
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    ParcelCreationResponse,
)
from catalystwan.models.configuration.feature_profile.sdwan.interest_groups import (
    INTEREST_GROUP_PAYLOAD_ENDPOINT_MAPPING,
    AnyInterestGroupParcel,
)


class SDRoutingFeatureProfilesAPI:
    def __init__(self, session: ManagerSession):
        self.cli = SDRoutingCLIFeatureProfileAPI(session=session)
        self.policy_object = PolicyObjectFeatureProfileAPI(session=session)


class FeatureProfileAPI(Protocol):
    def init_parcels(self, fp_id: str) -> None:
        """
        Initialized parcel(s) associated with this feature profile
        """
        ...

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates feature profile
        """
        ...

    def delete(self, fp_id: str) -> None:
        """
        Deletes feature profile
        """
        ...


class SDRoutingCLIFeatureProfileAPI(FeatureProfileAPI):
    """
    SD-Routing CLI feature-profile APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def init_parcels(self, fp_id: str) -> None:
        """
        Initialize CLI full-config parcel associated with this feature profile
        """
        self.full_config_parcel = SDRoutingFullConfigParcelAPI(session=self.session, fp_id=fp_id)

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates CLI feature profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)

        return self.endpoint.create_cli_feature_profile(payload=payload)

    def delete(self, fp_id: str) -> None:
        """
        Deletes CLI feature-profile
        """
        self.endpoint.delete_cli_feature_profile(cli_fp_id=fp_id)


class PolicyObjectFeatureProfileAPI:
    """
    SDWAN Feature Profile Policy Object APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = PolicyObjectFeatureProfile(session)

    # def get(self, profile: FeatureProfileInfo,
    #    get_by_type: AnyPolicyParcel,
    #    get_by_id: Union[UUID, None] = None):
    #     if not get_by_id:
    #         policy_object_list_type = PAYLOAD_ENDPOINT_MAPPING[get_by_type]
    #         return self.endpoint.get_all(profile_id=profile.profile_id,
    #    policy_object_list_type=policy_object_list_type)

    def create(self, profile: FeatureProfileInfo, payload: AnyInterestGroupParcel) -> ParcelCreationResponse:
        """
        Create Policy Object for selected profile based on payload type
        """

        profile_id = profile.profile_id
        policy_object_list_type = INTEREST_GROUP_PAYLOAD_ENDPOINT_MAPPING[type(payload)]
        return self.endpoint.create(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, payload=payload
        )

    def update(self, profile: FeatureProfileInfo, payload: AnyInterestGroupParcel, list_object_id: UUID):
        """
        Update Policy Object for selected profile based on payload type
        """
        profile_id = profile.profile_id
        policy_type = INTEREST_GROUP_PAYLOAD_ENDPOINT_MAPPING[type(payload)]
        return self.endpoint.update(
            profile_id=profile_id, policy_object_list_type=policy_type, list_object_id=list_object_id, payload=payload
        )

    def delete(self, profile: FeatureProfileInfo, policy_type: AnyInterestGroupParcel, list_object_id: UUID):
        """
        Delete Policy Object for selected profile based on payload type
        """
        profile_id = profile.profile_id
        policy_object_list_type = INTEREST_GROUP_PAYLOAD_ENDPOINT_MAPPING[type(policy_type)]
        return self.endpoint.delete(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=list_object_id
        )
