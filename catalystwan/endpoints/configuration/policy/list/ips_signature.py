# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.policy.lists import IPSSignatureList
from catalystwan.models.policy.policy_list import (
    InfoTag,
    PolicyListEndpoints,
    PolicyListId,
    PolicyListInfo,
    PolicyListPreview,
)
from catalystwan.typed_list import DataSequence


class IPSSignatureListEditPayload(IPSSignatureList, PolicyListId):
    pass


class IPSSignatureListInfo(IPSSignatureList, PolicyListInfo):
    pass


class ConfigurationPolicyIPSSignatureList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/ipssignature")
    def create_policy_list(self, payload: IPSSignatureList) -> PolicyListId:
        ...

    @delete("/template/policy/list/ipssignature/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/ipssignature")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/ipssignature/{id}")
    def edit_policy_list(self, id: UUID, payload: IPSSignatureListEditPayload) -> None:
        ...

    @get("/template/policy/list/ipssignature/{id}")
    def get_lists_by_id(self, id: UUID) -> IPSSignatureListInfo:
        ...

    @get("/template/policy/list/ipssignature", "data")
    def get_policy_lists(self) -> DataSequence[IPSSignatureListInfo]:
        ...

    @get("/template/policy/list/ipssignature/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[IPSSignatureListInfo]:
        ...

    @post("/template/policy/list/ipssignature/preview")
    def preview_policy_list(self, payload: IPSSignatureList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/ipssignature/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
