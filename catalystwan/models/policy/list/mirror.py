# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from catalystwan.models.policy.lists_entries import MirrorListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class MirrorList(PolicyListBase):
    type: Literal["mirror"] = "mirror"
    entries: List[MirrorListEntry] = []


class MirrorListEditPayload(MirrorList, PolicyListId):
    pass


class MirrorListInfo(MirrorList, PolicyListInfo):
    pass
