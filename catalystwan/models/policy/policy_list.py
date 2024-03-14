# Copyright 2023 Cisco Systems, Inc. and its affiliates

import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PolicyListBase(BaseModel):
    name: str = Field(
        pattern="^[a-zA-Z0-9_-]{1,32}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 32 characters",
    )
    description: Optional[str] = "Desc Not Required"
    entries: List[Any]

    def _add_entry(self, entry: Any, single: bool = False) -> None:
        if self.entries and single:
            self.entries[0] = entry
            del self.entries[1:]
        else:
            self.entries.append(entry)


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
