# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.definitions.zone_based_firewall import ZoneBasedFWPolicy, ZoneBasedFWPolicyDefinition
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionBuilder,
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class ZoneBasedFWPolicyCreationPayload(ZoneBasedFWPolicy):
    definition: ZoneBasedFWPolicyDefinition


class ZoneBasedFWPolicyGetResponse(ZoneBasedFWPolicyCreationPayload, PolicyDefinitionId):
    pass


class ZoneBasedFWPolicyEditPayload(ZoneBasedFWPolicyCreationPayload, PolicyDefinitionId):
    pass


class ZoneBasedFWPolicyInfo(ZoneBasedFWPolicy, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyZoneBasedFirewallDefinitionBuilder(APIEndpoints, PolicyDefinitionBuilder):
    @post("/template/policy/definition/zonebasedfw")
    def create_policy_definition(self, payload: ZoneBasedFWPolicyCreationPayload) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/zonebasedfw/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/zonebasedfw/multiple/{id}
        ...

    @put("/template/policy/definition/zonebasedfw/{id}")
    def edit_policy_definition(self, id: str, payload: ZoneBasedFWPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/zonebasedfw", "data")
    def get_definitions(self) -> DataSequence[ZoneBasedFWPolicyInfo]:
        ...

    @get("/template/policy/definition/zonebasedfw/{id}")
    def get_policy_definition(self, id: str) -> ZoneBasedFWPolicyGetResponse:
        ...

    @post("/template/policy/definition/zonebasedfw/preview")
    def preview_policy_definition(self, payload: ZoneBasedFWPolicyCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/zonebasedfw/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/zonebasedfw/bulk
        ...
