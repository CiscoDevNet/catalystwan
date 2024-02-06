# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import PolicerList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class PolicerListEditPayload(PolicerList, PolicyListId):
    pass


class PolicerListInfo(PolicerList, PolicyListInfo):
    pass


class ConfigurationPolicyPolicerClassList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/policer")
    def create_policy_list(self, payload: PolicerList) -> PolicyListId:
        ...

    @delete("/template/policy/list/policer/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/policer")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/policer/{id}")
    def edit_policy_list(self, id: UUID, payload: PolicerListEditPayload) -> None:
        ...

    @get("/template/policy/list/policer/{id}")
    def get_lists_by_id(self, id: UUID) -> PolicerListInfo:
        ...

    @get("/template/policy/list/policer", "data")
    def get_policy_lists(self) -> DataSequence[PolicerListInfo]:
        ...

    @get("/template/policy/list/policer/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[PolicerListInfo]:
        ...

    @post("/template/policy/list/policer/preview")
    def preview_policy_list(self, payload: PolicerList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/policer/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
