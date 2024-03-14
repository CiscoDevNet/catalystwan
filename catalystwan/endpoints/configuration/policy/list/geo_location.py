# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.geo_location import GeoLocationList, GeoLocationListEditPayload, GeoLocationListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyGeoLocationList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/geolocation")
    def create_policy_list(self, payload: GeoLocationList) -> PolicyListId:
        ...

    @delete("/template/policy/list/geolocation/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/geolocation")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/geolocation/{id}")
    def edit_policy_list(self, id: UUID, payload: GeoLocationListEditPayload) -> None:
        ...

    @get("/template/policy/list/geolocation/{id}")
    def get_lists_by_id(self, id: UUID) -> GeoLocationListInfo:
        ...

    @get("/template/policy/list/geolocation", "data")
    def get_policy_lists(self) -> DataSequence[GeoLocationListInfo]:
        ...

    @get("/template/policy/list/geolocation/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[GeoLocationListInfo]:
        ...

    @post("/template/policy/list/geolocation/preview")
    def preview_policy_list(self, payload: GeoLocationList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/geolocation/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
