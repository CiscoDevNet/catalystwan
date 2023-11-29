from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.model.policy.policy_definition import PLPEntryValues, PolicyDefinitionBody, PolicyDefinitionHeader


class RewritePolicyHeader(PolicyDefinitionHeader):
    type: Literal["rewriteRule"] = "rewriteRule"


class RewritePolicyRule(BaseModel):
    class_: str = Field(alias="class")
    plp: str
    dscp: str
    l2cos: str = Field(alias="layer2Cos")
    model_config = ConfigDict(populate_by_name=True)


class RewritePolicyDefinition(BaseModel):
    rules: List[RewritePolicyRule] = []


class RewritePolicy(RewritePolicyHeader, PolicyDefinitionBody):
    definition: RewritePolicyDefinition = RewritePolicyDefinition()

    def add_rule(self, class_map_ref: str, dscp: int, l2cos: int, plp: PLPEntryValues) -> None:
        self.definition.rules.append(
            RewritePolicyRule(class_=class_map_ref, plp=plp, dscp=str(dscp), l2cos=str(l2cos))  # type: ignore[call-arg]
        )

    model_config = ConfigDict(populate_by_name=True)
