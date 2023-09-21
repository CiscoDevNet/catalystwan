import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from vmngclient.model.policy.lists import AllPolicyLists

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
