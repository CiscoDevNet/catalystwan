# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class IPSSignatureListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    generator_id: str = Field(serialization_alias="generatorId", validation_alias="generatorId")
    signature_id: str = Field(serialization_alias="signatureId", validation_alias="signatureId")


class IPSSignatureList(PolicyListBase):
    type: Literal["ipsSignature"] = "ipsSignature"
    entries: List[IPSSignatureListEntry] = []


class IPSSignatureListEditPayload(IPSSignatureList, PolicyListId):
    pass


class IPSSignatureListInfo(IPSSignatureList, PolicyListInfo):
    pass
