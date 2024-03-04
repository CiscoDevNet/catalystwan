# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put
from catalystwan.models.policy.security import (
    AnySecurityPolicy,
    SecurityPolicyEditResponse,
    SecurityPolicyInfoRoot,
    SecurityPolicyRoot,
)
from catalystwan.typed_list import DataSequence


class ConfigurationSecurityTemplatePolicy(APIEndpoints):
    @post("/template/policy/security")
    def create_security_template(self, payload: AnySecurityPolicy) -> None:
        ...

    @delete("/template/policy/security/{id}")
    def delete_security_template(self, id: UUID, payload: JSON = {}) -> None:
        ...

    @put("/template/policy/security/{id}")
    def edit_security_template(self, id: UUID, payload: AnySecurityPolicy) -> SecurityPolicyEditResponse:
        # PUT /template/policy/security/{policyId}
        ...

    def edit_template_with_lenient_lock(self):
        # PUT /template/policy/security/staging/{policyId}
        ...

    def generate_security_policy_summary(self):
        # GET /template/policy/security/summary
        ...

    @get("/template/policy/security", "data")
    def generate_security_template_list(self) -> DataSequence[SecurityPolicyInfoRoot]:
        ...

    def get_device_list_by_id(self):
        # GET /template/policy/security/devices/{policyId}
        ...

    def get_security_policy_device_list(self):
        # GET /template/policy/security/devices
        ...

    @get("/template/policy/security/definition/{id}")
    def get_security_template(self, id: UUID) -> SecurityPolicyRoot:
        ...

    def get_security_templates_for_device(self):
        # GET /template/policy/security/{deviceModel}
        ...
