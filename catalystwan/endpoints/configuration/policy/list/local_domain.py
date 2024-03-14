# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.local_domain import LocalDomainList, LocalDomainListEditPayload, LocalDomainListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyLocalDomainList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/localdomain")
    def create_policy_list(self, payload: LocalDomainList) -> PolicyListId:
        ...

    @delete("/template/policy/list/localdomain/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/localdomain")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/localdomain/{id}")
    def edit_policy_list(self, id: UUID, payload: LocalDomainListEditPayload) -> None:
        ...

    @get("/template/policy/list/localdomain/{id}")
    def get_lists_by_id(self, id: UUID) -> LocalDomainListInfo:
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
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
