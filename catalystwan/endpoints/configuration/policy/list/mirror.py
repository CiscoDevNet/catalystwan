# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import MirrorList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class MirrorListEditPayload(MirrorList, PolicyListId):
    pass


class MirrorListInfo(MirrorList, PolicyListInfo):
    pass


class ConfigurationPolicyMirrorList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/mirror")
    def create_policy_list(self, payload: MirrorList) -> PolicyListId:
        ...

    @delete("/template/policy/list/mirror/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/mirror")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/mirror/{id}")
    def edit_policy_list(self, id: UUID, payload: MirrorListEditPayload) -> None:
        ...

    @get("/template/policy/list/mirror/{id}")
    def get_lists_by_id(self, id: UUID) -> MirrorListInfo:
        ...

    @get("/template/policy/list/mirror", "data")
    def get_policy_lists(self) -> DataSequence[MirrorListInfo]:
        ...

    @get("/template/policy/list/mirror/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[MirrorListInfo]:
        ...

    @post("/template/policy/list/mirror/preview")
    def preview_policy_list(self, payload: MirrorList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/mirror/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
