# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.lists import LocalDomainList
from vmngclient.model.policy.policy_list import (
    InfoTag,
    PolicyListBuilder,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class LocalDomainListEditPayload(LocalDomainList, PolicyListId):
    pass


class LocalDomainListInfo(LocalDomainList, PolicyListInfo):
    pass


class ConfigurationPolicyLocalDomainListBuilder(APIEndpoints, PolicyListBuilder):
    @post("/template/policy/list/localdomain")
    def create_policy_list(self, payload: LocalDomainList) -> PolicyListId:
        ...

    @delete("/template/policy/list/localdomain/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/localdomain")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/localdomain/{id}")
    def edit_policy_list(self, id: str, payload: LocalDomainListEditPayload) -> None:
        ...

    @get("/template/policy/list/localdomain/{id}")
    def get_lists_by_id(self, id: str) -> LocalDomainListInfo:
        ...

    @get("/template/policy/list/localdomain", "data")
    def get_policy_lists(self) -> DataSequence[LocalDomainListInfo]:
        ...

    @get("/template/policy/list/localdomain/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[LocalDomainListInfo]:
        ...

    @post("/template/policy/list/localdomain/preview")
    def preview_policy_list(self, payload: LocalDomainList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/localdomain/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
