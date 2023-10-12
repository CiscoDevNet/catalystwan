# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import GeoLocationList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class GeoLocationListEditPayload(GeoLocationList, PolicyListId):
    pass


class GeoLocationListInfo(GeoLocationList, PolicyListInfo):
    pass


class ConfigurationPolicyGeoLocationListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/geolocation")
    def create_policy_list(self, payload: GeoLocationList) -> PolicyListId:
        ...

    @delete("/template/policy/list/geolocation/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/geolocation")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/geolocation/{id}")
    def edit_policy_list(self, id: str, payload: GeoLocationListEditPayload) -> None:
        ...

    @get("/template/policy/list/geolocation/{id}")
    def get_lists_by_id(self, id: str) -> GeoLocationListInfo:
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
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
