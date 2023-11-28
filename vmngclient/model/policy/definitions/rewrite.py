from typing import List

from pydantic.v1 import BaseModel, Field

from vmngclient.model.policy.policy_definition import PLPEntryValues, PolicyDefinitionBody, PolicyDefinitionHeader


class RewritePolicyHeader(PolicyDefinitionHeader):
    type: str = Field(default="rewriteRule", const=True)


class RewritePolicyRule(BaseModel):
    class_: str = Field(alias="class")
    plp: str
    dscp: str
    l2cos: str = Field(alias="layer2Cos")

    class Config:
        allow_population_by_field_name = True


class RewritePolicyDefinition(BaseModel):
    rules: List[RewritePolicyRule] = []


class RewritePolicy(RewritePolicyHeader, PolicyDefinitionBody):
    definition: RewritePolicyDefinition = RewritePolicyDefinition()

    def add_rule(self, class_map_ref: str, dscp: int, l2cos: int, plp: PLPEntryValues) -> None:
        self.definition.rules.append(
            RewritePolicyRule(class_=class_map_ref, plp=plp, dscp=str(dscp), l2cos=str(l2cos))  # type: ignore[call-arg]
        )

    class Config:
        allow_population_by_field_name = True
