# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ProtocolNameListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    protocol_name: str = Field(serialization_alias="protocolName", validation_alias="protocolName")


class ProtocolNameList(PolicyListBase):
    type: Literal["protocolName"] = "protocolName"
    entries: List[ProtocolNameListEntry] = []


class ProtocolNameListEditPayload(ProtocolNameList, PolicyListId):
    pass


class ProtocolNameListInfo(ProtocolNameList, PolicyListInfo):
    pass
