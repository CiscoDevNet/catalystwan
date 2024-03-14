# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ASPathListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    as_path: str = Field(serialization_alias="asPath", validation_alias="asPath")


class ASPathList(PolicyListBase):
    type: Literal["asPath"] = "asPath"
    entries: List[ASPathListEntry] = []


class ASPathListEditPayload(ASPathList, PolicyListId):
    pass


class ASPathListInfo(ASPathList, PolicyListInfo):
    pass
