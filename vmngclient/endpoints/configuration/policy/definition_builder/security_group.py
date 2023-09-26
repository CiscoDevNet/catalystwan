# mypy: disable-error-code="empty-body"
from enum import Enum
from ipaddress import IPv4Network, IPv6Network
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, root_validator

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionHeader,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence


class SequenceIPType(str, Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"


class ListReference(BaseModel):
    ref: str


class VariableName(BaseModel):
    vip_variable_name: str = Field(alias="vipVariableName")


class SecurityGroupIPv4Definition(BaseModel):
    data_prefix: Union[IPv4Network, VariableName, None] = Field(None, alias="dataPrefix")
    data_prefix_list: Optional[ListReference] = Field(None, alias="dataPrefixList")
    fqdn: Optional[str] = None
    fqdn_list: Optional[ListReference] = Field(None, alias="fqdnList")
    geo_location: Optional[str] = Field(None, alias="geoLocation")
    geo_location_list: Optional[ListReference] = Field(None, alias="geoLocationList")
    port: Optional[str] = None
    port_list: Optional[ListReference] = Field(None, alias="portList")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def check_exclusive_fields(cls, values):
        if values.get("dataPrefix") is not None and values.get("dataPrefixList") is not None:
            raise ValueError("dataPrefix and dataPrefixList cannot be set at the same time")
        if values.get("fqdn") is not None and values.get("fqdnList") is not None:
            raise ValueError("fqdn and fqdnList cannot be set at the same time")
        if values.get("geoLocation") is not None and values.get("geoLocationList") is not None:
            raise ValueError("geoLocation and geoLocationList cannot be set at the same time")
        if values.get("port") is not None and values.get("portList") is not None:
            raise ValueError("port and portList cannot be set at the same time")
        return values


class SecurityGroupIPv6Definition(BaseModel):
    data_ipv6_prefix: Union[IPv6Network, VariableName, None] = Field(None, alias="dataIPV6Prefix")
    data_ipv6_prefix_list: Optional[ListReference] = Field(None, alias="dataIPV6PrefixList")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def check_exclusive_fields(cls, values):
        if values.get("dataIPV6Prefix") is not None and values.get("dataIPV6PrefixList") is not None:
            raise ValueError("dataPrefix and dataPrefixList cannot be set at the same time")
        return values


class SecurityGroup(PolicyDefinitionHeader):
    type: str = Field(default="securityGroup", const=True)
    mode: str = Field(default="unified", const=True)


class SecurityGroupDefinition(SecurityGroup):
    sequence_ip_type: SequenceIPType = Field(alias="sequenceIpType")
    definition: Union[SecurityGroupIPv4Definition, SecurityGroupIPv6Definition]

    @root_validator(pre=True)
    def validate_by_sequence_ip_type(cls, values):
        ip_type = values.get("sequenceIpType")
        definition = values.get("definition")
        if (ip_type == SequenceIPType.IPV4 and isinstance(definition, SecurityGroupIPv6Definition)) or (
            ip_type == SequenceIPType.IPV6 and isinstance(definition, SecurityGroupIPv4Definition)
        ):
            raise ValueError(f"Incompatible definition for {ip_type} sequence")
        return values


class SecurityGroupCreationPayload(SecurityGroupDefinition):
    pass


class SecurityGroupEditPayload(SecurityGroupCreationPayload, PolicyDefinitionId):
    pass


class SecurityGroupInfo(SecurityGroupDefinition, PolicyDefinitionId, PolicyDefinitionInfo):
    pass


class ConfigurationPolicySecurityGroupDefinitionBuilder(APIEndpoints):
    @post("/template/policy/definition/securitygroup")
    def create_policy_definition(self, payload: SecurityGroupCreationPayload) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/securitygroup/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/securitygroup/multiple/{id}
        ...

    @put("/template/policy/definition/securitygroup/{id}")
    def edit_policy_definition(self, id: str, payload: SecurityGroupEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/securitygroup", "data")
    def get_definitions(self) -> DataSequence[SecurityGroupInfo]:
        ...

    @get("/template/policy/definition/securitygroup/{id}")
    def get_policy_definition(self, id: str) -> SecurityGroupInfo:
        ...

    @post("/template/policy/definition/securitygroup/preview")
    def preview_policy_definition(self, payload: SecurityGroupCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/securitygroup/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/securitygroup/bulk
        ...
