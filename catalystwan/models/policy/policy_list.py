# Copyright 2023 Cisco Systems, Inc. and its affiliates

import datetime
from typing import List, Optional, Protocol
from uuid import UUID

from pydantic import BaseModel, Field

from catalystwan.models.policy import AnyPolicyList
from catalystwan.typed_list import DataSequence


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", alias="infoTag")


class PolicyListId(BaseModel):
    list_id: UUID = Field(alias="listId")


class PolicyListInfo(PolicyListId, InfoTag):
    last_updated: datetime.datetime = Field(alias="lastUpdated")
    owner: str
    read_only: bool = Field(alias="readOnly")
    version: str
    reference_count: int = Field(alias="referenceCount")
    references: List
    is_activated_by_vsmart: Optional[bool] = Field(None, alias="isActivatedByVsmart")


class PolicyListPreview(BaseModel):
    preview: str


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
