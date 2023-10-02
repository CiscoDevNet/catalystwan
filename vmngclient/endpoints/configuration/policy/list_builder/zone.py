# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import ZoneList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class ZoneListEditPayload(ZoneList, PolicyListId):
    pass


class ZoneListInfo(ZoneList, PolicyListInfo):
    pass


class ConfigurationPolicyZoneListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/zone")
    def create_policy_list(self, payload: ZoneList) -> PolicyListId:
        ...

    @delete("/template/policy/list/zone/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/zone")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/zone/{id}")
    def edit_policy_list(self, id: str, payload: ZoneListEditPayload) -> None:
        ...

    @get("/template/policy/list/zone/{id}")
    def get_lists_by_id(self, id: str) -> ZoneListInfo:
        ...

    @get("/template/policy/list/zone", "data")
    def get_policy_lists(self) -> DataSequence[ZoneListInfo]:
        ...

    @get("/template/policy/list/zone/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ZoneListInfo]:
        ...

    @post("/template/policy/list/zone/preview")
    def preview_policy_list(self, payload: ZoneList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/zone/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
