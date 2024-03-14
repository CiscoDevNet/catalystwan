# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class URLListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pattern: str


class URLAllowList(PolicyListBase):
    type: Literal["urlWhiteList"] = "urlWhiteList"
    entries: List[URLListEntry] = []


class URLAllowListEditPayload(URLAllowList, PolicyListId):
    pass


class URLAllowListInfo(URLAllowList, PolicyListInfo):
    pass


class URLBlockList(PolicyListBase):
    type: Literal["urlBlackList"] = "urlBlackList"
    entries: List[URLListEntry] = []


class URLBlockListEditPayload(URLBlockList, PolicyListId):
    pass


class URLBlockListInfo(URLBlockList, PolicyListInfo):
    pass
