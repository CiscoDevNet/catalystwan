# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put


class ConfigurationVEdgeTemplatePolicy(APIEndpoints):
    def change_policy_resource_group(self):
        # POST /template/policy/vedge/{resourceGroupName}/{policyId}
        ...

    @post("/template/policy/vedge")
    def create_vedge_template(self):
        # POST /template/policy/vedge
        ...

    @delete("/template/policy/vedge/{id}")
    def delete_vedge_template(self, id: str):
        # DELETE /template/policy/vedge/{policyId}
        ...

    @put("/template/policy/vedge/{id}")
    def edit_vedge_template(self, id: str):
        # PUT /template/policy/vedge/{policyId}
        ...

    @get("/template/policy/vedge", "data")
    def generate_policy_template_list(self):
        # GET /template/policy/vedge
        ...

    @get("/template/policy/vedge/devices/{id}")
    def get_device_list_by_policy(self):
        # GET /template/policy/vedge/devices/{policyId}
        ...

    @get("/template/policy/vedge/devices")
    def get_vedge_policy_device_list(self):
        # GET /template/policy/vedge/devices
        ...

    @get("/template/policy/vedge/definition/{id}")
    def get_vedge_template(self):
        # GET /template/policy/vedge/definition/{policyId}
        ...
