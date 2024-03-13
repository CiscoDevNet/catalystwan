# Copyright 2023 Cisco Systems, Inc. and its affiliates

import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


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
