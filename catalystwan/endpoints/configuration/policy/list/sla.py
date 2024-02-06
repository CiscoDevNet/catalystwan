# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import SLAClassList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class SLAClassListEditPayload(SLAClassList, PolicyListId):
    pass


class SLAClassListInfo(SLAClassList, PolicyListInfo):
    pass


class ConfigurationPolicySLAClassList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/sla")
    def create_policy_list(self, payload: SLAClassList) -> PolicyListId:
        ...

    @delete("/template/policy/list/sla/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/sla")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/sla/{id}")
    def edit_policy_list(self, id: UUID, payload: SLAClassListEditPayload) -> None:
        ...

    @get("/template/policy/list/sla/{id}")
    def get_lists_by_id(self, id: UUID) -> SLAClassListInfo:
        ...

    @get("/template/policy/list/sla", "data")
    def get_policy_lists(self) -> DataSequence[SLAClassListInfo]:
        ...

    @get("/template/policy/list/sla/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SLAClassListInfo]:
        ...

    @post("/template/policy/list/sla/preview")
    def preview_policy_list(self, payload: SLAClassList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/sla/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
