# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import JSON, APIEndpoints, delete, get, post, put
from vmngclient.model.policy.security import SecurityPolicy, SecurityPolicyEditResponse, SecurityPolicyInfo
from vmngclient.typed_list import DataSequence


class ConfigurationSecurityTemplatePolicy(APIEndpoints):
    @post("/template/policy/security")
    def create_security_template(self, payload: SecurityPolicy) -> None:
        ...

    @delete("/template/policy/security/{id}")
    def delete_security_template(self, id: str, payload: JSON = {}) -> None:
        ...

    @put("/template/policy/security/{id}")
    def edit_security_template(self, id: str, payload: SecurityPolicy) -> SecurityPolicyEditResponse:
        # PUT /template/policy/security/{policyId}
        ...

    def edit_template_with_lenient_lock(self):
        # PUT /template/policy/security/staging/{policyId}
        ...

    def generate_security_policy_summary(self):
        # GET /template/policy/security/summary
        ...

    @get("/template/policy/security", "data")
    def generate_security_template_list(self) -> DataSequence[SecurityPolicyInfo]:
        ...

    def get_device_list_by_id(self):
        # GET /template/policy/security/devices/{policyId}
        ...

    def get_security_policy_device_list(self):
        # GET /template/policy/security/devices
        ...

    @get("/template/policy/security/definition/{id}")
    def get_security_template(self, id: str) -> SecurityPolicy:
        ...

    def get_security_templates_for_device(self):
        # GET /template/policy/security/{deviceModel}
        ...
