# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    DefinitionWithSequencesCommonBase,
    PLPEntryType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)


class RewritePolicyHeader(PolicyDefinitionBase):
    type: Literal["rewriteRule"] = "rewriteRule"


class RewritePolicyRule(BaseModel):
    class_: UUID = Field(serialization_alias="class", validation_alias="class")
    plp: str
    dscp: str
    l2cos: str = Field(serialization_alias="layer2Cos", validation_alias="layer2Cos")
    model_config = ConfigDict(populate_by_name=True)


class RewritePolicyDefinition(BaseModel):
    rules: List[RewritePolicyRule] = []


class RewritePolicy(RewritePolicyHeader, DefinitionWithSequencesCommonBase):
    definition: RewritePolicyDefinition = RewritePolicyDefinition()

    def add_rule(self, class_map_ref: UUID, dscp: int, l2cos: int, plp: PLPEntryType) -> None:
        self.definition.rules.append(RewritePolicyRule(class_=class_map_ref, plp=plp, dscp=str(dscp), l2cos=str(l2cos)))

    model_config = ConfigDict(populate_by_name=True)


class RewritePolicyEditPayload(RewritePolicy, PolicyDefinitionId):
    pass


class RewritePolicyGetResponse(RewritePolicy, PolicyDefinitionGetResponse):
    pass
