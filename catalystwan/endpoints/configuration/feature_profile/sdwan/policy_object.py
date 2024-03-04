# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import Parcel, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.typed_list import DataSequence


class PolicyObjectFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/policy-object/{profile_id}/{policy_object_list_type}")
    def create(
        self, profile_id: UUID, policy_object_list_type: str, payload: AnyPolicyObjectParcel
    ) -> ParcelCreationResponse:
        ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @post("/v1/feature-profile/sdwan/policy-object/{policy_object_id}/unified/{security_object_list_type}")
    # def create_security_profile_parcel(self, policy_object_id: UUID, security_object_list_type: str):
    #     ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/policy-object/{profile_id}/{policy_object_list_type}/{list_object_id}")
    def delete(self, profile_id: UUID, policy_object_list_type: str, list_object_id: UUID) -> None:
        ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @delete(
    #     "/v1/feature-profile/sdwan/policy-object/{policy_object_id}/unified/{security_object_list_type}/{security_profile_parcel_id}"
    # )
    # def delete_security_profile_parcel1(
    #     self, policy_object_id: UUID, security_object_list_type: str, security_profile_parcel_id: UUID
    # ):
    #     ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/policy-object/{profile_id}/{policy_object_list_type}/{list_object_id}")
    def update(
        self, profile_id: UUID, policy_object_list_type: str, list_object_id: UUID, payload: AnyPolicyObjectParcel
    ) -> ParcelCreationResponse:
        ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @put(
    #     "/v1/feature-profile/sdwan/policy-object/{policy_object_id}/unified/{security_object_list_type}/{security_profile_parcel_id}"
    # )
    # def edit_security_profile_parcel1(
    #     self, policy_object_id: UUID, security_object_list_type: str, security_profile_parcel_id: UUID
    # ):
    #     ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/policy-object/{profile_id}/{policy_object_list_type}/{list_object_id}")
    def get_by_id(self, profile_id: UUID, policy_object_list_type: str, list_object_id: UUID) -> Parcel:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/policy-object/{profile_id}/{policy_object_list_type}", resp_json_key="data")
    def get_all(self, profile_id: UUID, policy_object_list_type: str) -> DataSequence[Parcel]:
        ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @get("/v1/feature-profile/sdwan/policy-object/{policy_object_list_type}/schema")
    # def get_sdwan_policy_object_data_prefix_parcel_schema_by_schema_type(self, policy_object_list_type: str):
    #     ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @get("/v1/feature-profile/sdwan/policy-object/{policy_object_id}/unified/{security_object_list_type}")
    # def get_security_profile_parcel(self, policy_object_id: UUID, security_object_list_type: str):
    #     ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @get(
    #     "/v1/feature-profile/sdwan/policy-object/{policy_object_id}/unified/{security_object_list_type}/{security_profile_parcel_id}"
    # )
    # def get_security_profile_parcel_by_parcel_id(
    #     self, policy_object_id: UUID, security_object_list_type: str, security_profile_parcel_id: UUID
    # ):
    #     ...
