import datetime
from typing import List, Optional, Protocol

from pydantic.v1 import BaseModel, Field

from vmngclient.model.policy.lists import AllPolicyLists
from vmngclient.typed_list import DataSequence

PolicyList = AllPolicyLists


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", alias="infoTag")


class PolicyListId(BaseModel):
    list_id: str = Field(alias="listId")


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


class PolicyListBuilder(Protocol):
    def create_policy_list(self, payload: BaseModel) -> PolicyListId:
        ...

    def delete_policy_list(self, id: str) -> None:
        ...

    def edit_policy_list(self, id: str, payload: BaseModel) -> None:
        ...

    def get_lists_by_id(self, id: str) -> BaseModel:
        ...

    def get_policy_lists(self) -> DataSequence[BaseModel]:
        ...
