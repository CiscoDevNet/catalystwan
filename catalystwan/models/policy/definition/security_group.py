# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network, IPv6Network
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.models.common import check_any_of_exclusive_field_sets, check_fields_exclusive
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
    VariableName,
)

SequenceIPType = Literal[
    "ipv4",
    "ipv6",
]


class SecurityGroupIPv4Definition(BaseModel):
    data_prefix: Union[IPv4Network, VariableName, None] = Field(None, alias="dataPrefix")
    data_prefix_list: Optional[Reference] = Field(None, alias="dataPrefixList")
    fqdn: Optional[str] = None
    fqdn_list: Optional[Reference] = Field(None, alias="fqdnList")
    geo_location: Optional[str] = Field(None, alias="geoLocation")
    geo_location_list: Optional[Reference] = Field(None, alias="geoLocationList")
    port: Optional[str] = None
    port_list: Optional[Reference] = Field(None, alias="portList")
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        check_any_of_exclusive_field_sets(
            self.__dict__,
            [
                ({"data_prefix", "data_prefix_list"}, False),
                ({"fqdn", "fqdn_list"}, False),
                ({"geo_location", "geo_location_list"}, False),
                ({"port", "port_list"}, False),
            ],
        )
        return self


class SecurityGroupIPv6Definition(BaseModel):
    data_ipv6_prefix: Union[IPv6Network, VariableName, None] = Field(None, alias="dataIPV6Prefix")
    data_ipv6_prefix_list: Optional[Reference] = Field(None, alias="dataIPV6PrefixList")
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        check_fields_exclusive(self.__dict__, {"data_ipv6_prefix", "data_ipv6_prefix_list"}, True)
        return self


class SecurityGroup(PolicyDefinitionBase):
    # TODO: cannot use sequence_ip_type discriminated unions here as this is root of model
    # EndpointAPI would need to support annotated union as payload parameter
    type: Literal["securityGroup"] = "securityGroup"
    mode: Literal["unified"] = "unified"
    sequence_ip_type: SequenceIPType = Field(alias="sequenceIpType")
    definition: Union[SecurityGroupIPv4Definition, SecurityGroupIPv6Definition]

    @model_validator(mode="after")
    def validate_by_sequence_ip_type(self):
        if (
            self.sequence_ip_type == SequenceIPType.IPV4 and isinstance(self.definition, SecurityGroupIPv6Definition)
        ) or (
            self.sequence_ip_type == SequenceIPType.IPV6 and isinstance(self.definition, SecurityGroupIPv4Definition)
        ):
            raise ValueError(f"Incompatible definition for {self.sequence_ip_type} sequence")
        return self


class SecurityGroupEditPayload(SecurityGroup, PolicyDefinitionId):
    pass


class SecurityGroupGetResponse(SecurityGroup, PolicyDefinitionGetResponse):
    pass
