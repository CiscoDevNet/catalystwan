# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class LocalDomainListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name_server: str = Field(
        pattern="^[^*+].*",
        serialization_alias="nameServer",
        validation_alias="nameServer",
        max_length=240,
        description="Must be valid std regex."
        "String cannot start with a '*' or a '+', be empty, or be more than 240 characters",
    )


class LocalDomainList(PolicyListBase):
    type: Literal["localDomain"] = "localDomain"
    entries: List[LocalDomainListEntry] = []


class LocalDomainListEditPayload(LocalDomainList, PolicyListId):
    pass


class LocalDomainListInfo(LocalDomainList, PolicyListInfo):
    pass
