# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.local_app import LocalAppList, LocalAppListEditPayload, LocalAppListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyLocalAppList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/localapp")
    def create_policy_list(self, payload: LocalAppList) -> PolicyListId:
        ...

    @delete("/template/policy/list/localapp/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/localapp")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/localapp/{id}")
    def edit_policy_list(self, id: UUID, payload: LocalAppListEditPayload) -> None:
        ...

    @get("/template/policy/list/localapp/{id}")
    def get_lists_by_id(self, id: UUID) -> LocalAppListInfo:
        ...

    @get("/template/policy/list/localapp", "data")
    def get_policy_lists(self) -> DataSequence[LocalAppListInfo]:
        ...

    @get("/template/policy/list/localapp/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[LocalAppListInfo]:
        ...

    @post("/template/policy/list/localapp/preview")
    def preview_policy_list(self, payload: LocalAppList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/localapp/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
