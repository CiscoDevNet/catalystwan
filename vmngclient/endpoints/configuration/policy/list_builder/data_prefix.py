# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import DataPrefixList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class DataPrefixListEditPayload(DataPrefixList, PolicyListId):
    pass


class DataPrefixListInfo(DataPrefixList, PolicyListInfo):
    pass


class ConfigurationPolicyDataPrefixListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/dataprefix")
    def create_policy_list(self, payload: DataPrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/dataprefix/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/dataprefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/dataprefix/{id}")
    def edit_policy_list(self, id: str, payload: DataPrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/dataprefix/{id}")
    def get_lists_by_id(self, id: str) -> DataPrefixListInfo:
        ...

    @get("/template/policy/list/dataprefix", "data")
    def get_policy_lists(self) -> DataSequence[DataPrefixListInfo]:
        ...

    @get("/template/policy/list/dataprefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[DataPrefixListInfo]:
        ...

    @post("/template/policy/list/dataprefix/preview")
    def preview_policy_list(self, payload: DataPrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/dataprefix/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
