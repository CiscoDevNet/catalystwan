from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from catalystwan.models.policy import AnyPolicyList
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
)
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo
from catalystwan.typed_list import DataSequence


class PolicyListEndpoints(Protocol):
    def create_policy_list(self, payload: AnyPolicyList) -> PolicyListId:
        ...

    def delete_policy_list(self, id: UUID) -> None:
        ...

    def edit_policy_list(self, id: UUID, payload: AnyPolicyList) -> None:
        ...

    def get_lists_by_id(self, id: UUID) -> PolicyListInfo:
        ...

    def get_policy_lists(self) -> DataSequence[PolicyListInfo]:
        ...


class PolicyDefinitionEndpoints(Protocol):
    def create_policy_definition(self, payload: BaseModel) -> PolicyDefinitionId:
        ...

    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_policy_definition(self, id: UUID, payload: BaseModel) -> PolicyDefinitionEditResponse:
        ...

    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    def get_policy_definition(self, id: UUID) -> PolicyDefinitionGetResponse:
        ...
