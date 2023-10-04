from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.endpoints.configuration_feature_profile import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    ParcelId,
    SDRoutingConfigurationFeatureProfile,
)
from vmngclient.model.feature_profile_parcel import FullConfig, FullConfigParcel
from vmngclient.typed_list import DataSequence


class SDRoutingFeatureProfileAPI:
    """
    SD-Routing feature-profile APIs
    """

    def __init__(self, session: vManageSession):
        self.session = session
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def create_cli_feature_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates CLI feature profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)

        return self.endpoint.create_cli_feature_profile(payload=payload)

    def create_cli_full_config_parcel(self, cli_fp_id: str, name: str, description: str, fullconfig: str) -> ParcelId:
        """
        Creates CLI full-config parcel
        """
        payload = FullConfigParcel(name=name, description=description, data=FullConfig(fullconfig=fullconfig))

        return self.endpoint.create_cli_full_config_parcel(cli_fp_id=cli_fp_id, payload=payload)

    def delete_cli_feature_profile(self, cli_fp_id: str) -> None:
        """
        Deletes CLI feature-profile
        """
        self.endpoint.delete_cli_feature_profile(cli_fp_id=cli_fp_id)

    def delete_cli_full_config_parcel(self, cli_fp_id: str, parcel_id: str) -> None:
        """
        Deletes CLI full-config parcel
        """
        self.endpoint.delete_cli_full_config_parcel(cli_fp_id=cli_fp_id, parcel_id=parcel_id)

    def edit_cli_full_config_parcel(
        self, cli_fp_id: str, parcel_id: str, name: str, description: str, fullconfig: str
    ) -> None:
        """
        Modifies existing CLI full-config parcel
        """
        payload = FullConfigParcel(name=name, description=description, data=FullConfig(fullconfig=fullconfig))

        self.endpoint.edit_cli_full_config_parcel(cli_fp_id=cli_fp_id, parcel_id=parcel_id, payload=payload)

    def get_cli_feature_profiles(self, limit: int = 0, offset: int = 0) -> DataSequence[FeatureProfileInfo]:
        """
        Gets existing CLI feature profiles
        """
        payload = GetFeatureProfilesPayload(limit=limit, offset=offset)

        return self.endpoint.get_cli_feature_profiles(payload=payload)
