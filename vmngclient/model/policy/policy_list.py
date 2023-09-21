import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", alias="infoTag")


class PolicyListId(BaseModel):
    list_id: str = Field(alias="listId")


class PolicyList(BaseModel):
    name: str = Field(
        regex="^[a-zA-Z0-9_-]{1,32}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 32 characters",
    )
    description: Optional[str] = "Desc Not Required"
    type: str
    entries: List


class PolicyListInfo(PolicyListId, InfoTag):
    last_updated: datetime.datetime = Field(alias="lastUpdated")
    owner: str
    read_only: bool = Field(alias="readOnly")
    version: str
    reference_count: int = Field(alias="referenceCount")
    references: List
    is_activated_by_vsmart: Optional[bool] = Field(None, alias="isActivatedByVsmart")


class PolicyListEditPayload(PolicyList, PolicyListId):
    pass


class PolicyListPreview(BaseModel):
    preview: str
