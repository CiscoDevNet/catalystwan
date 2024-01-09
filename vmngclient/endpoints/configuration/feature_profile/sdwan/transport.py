# mypy: disable-error-code="empty-body"

from typing import Optional

from vmngclient.api.configuration_groups.parcel import MainParcel
from vmngclient.endpoints import JSON, APIEndpoints, delete, get, post, versions
from vmngclient.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    ParcelId,
    SchemaTypeQuery,
)
from vmngclient.typed_list import DataSequence


class TransportFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_sdwan_transport_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/cellular-controller/schema", resp_json_key="request")
    def get_sdwan_transport_cellular_controller_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport")
    def create_sdwan_transport_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{transport_id}")
    def delete_sdwan_transport_feature_profile(self, transport_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{transport_id}/cellular-controller")
    def create_cellular_controller_profile_parcel_for_transport(
        self, transport_id: str, payload: MainParcel
    ) -> ParcelId:
        ...
