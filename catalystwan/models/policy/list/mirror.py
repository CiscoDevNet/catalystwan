# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class MirrorListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    remote_dest: IPvAnyAddress = Field(serialization_alias="remoteDest", validation_alias="remoteDest")
    source: IPvAnyAddress


class MirrorList(PolicyListBase):
    type: Literal["mirror"] = "mirror"
    entries: List[MirrorListEntry] = []


class MirrorListEditPayload(MirrorList, PolicyListId):
    pass


class MirrorListInfo(MirrorList, PolicyListInfo):
    pass
