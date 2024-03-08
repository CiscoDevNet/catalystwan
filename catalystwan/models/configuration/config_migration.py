# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from pydantic import BaseModel, Field

from catalystwan.models.policy import (
    AnyPolicyDefinition,
    AnyPolicyList,
    CentralizedPolicy,
    LocalizedPolicy,
    SecurityPolicy,
)


class UX1Policies(BaseModel):
    centralized_policies: List[CentralizedPolicy] = Field(default=[], serialization_alias="centralizedPolicies")
    localized_policies: List[LocalizedPolicy] = Field(default=[], serialization_alias="localizedPolicies")
    security_policies: List[SecurityPolicy] = Field(default=[], serialization_alias="securityPolicies")
    policy_definitions: List[AnyPolicyDefinition] = Field(default=[], serialization_alias="policyDefinitions")
    policy_lists: List[AnyPolicyList] = Field(default=[], serialization_alias="policyLists")


class UX1Templates(BaseModel):
    pass


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    policies: UX1Policies
    templates: UX1Templates


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    pass
