# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import AppProbeClassList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class AppProbeClassListEditPayload(AppProbeClassList, PolicyListId):
    pass


class AppProbeClassListInfo(AppProbeClassList, PolicyListInfo):
    pass


class ConfigurationPolicyAppProbeClassListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/appprobe")
    def create_policy_list(self, payload: AppProbeClassList) -> PolicyListId:
        ...

    @delete("/template/policy/list/appprobe/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/appprobe")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/appprobe/{id}")
    def edit_policy_list(self, id: str, payload: AppProbeClassListEditPayload) -> None:
        ...

    @get("/template/policy/list/appprobe/{id}")
    def get_lists_by_id(self, id: str) -> AppProbeClassListInfo:
        ...

    @get("/template/policy/list/appprobe", "data")
    def get_policy_lists(self) -> DataSequence[AppProbeClassListInfo]:
        ...

    @get("/template/policy/list/appprobe/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[AppProbeClassListInfo]:
        ...

    @post("/template/policy/list/appprobe/preview")
    def preview_policy_list(self, payload: AppProbeClassList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/appprobe/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
