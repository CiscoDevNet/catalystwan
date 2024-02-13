from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Union, overload
from uuid import UUID

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.api.parcel_api import SDRoutingFullConfigParcelAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.policy_object import PolicyObjectFeatureProfile
from catalystwan.endpoints.configuration_feature_profile import (
    ConfigurationFeatureProfile,
    SDRoutingConfigurationFeatureProfile,
)
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.payload_type import AnyPolicyObjectParcel


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
        self.configuration_feature_profile = ConfigurationFeatureProfile(session)

    @overload
    def create(self, profile: UUID, payload: AnyPolicyObjectParcel) -> None:
        ...

    @overload
    def create(self, profile: str, payload: AnyPolicyObjectParcel) -> None:
        ...

    def create(self, profile: Union[UUID, str], payload: AnyPolicyObjectParcel) -> None:
        """
        Creates Policy Object for selected profile based on payload type
        """

        profile_id = profile
        if isinstance(profile, str):
            profile_id = (
                self.configuration_feature_profile.get_sdwan_feature_profiles()
                .filter(profile_name=profile)
                .single_or_default()
                .profile_id
            )

        return self.endpoint.create(
            profile_id=profile_id, policy_object_list_type=payload._payload_endpoint.value, payload=payload
        )
