# mypy: disable-error-code="empty-body"
from enum import Enum
from ipaddress import IPv4Network, IPv6Network
from typing import Optional, Union

from pydantic.v1 import BaseModel, Extra, Field, root_validator

from vmngclient.model.common import check_any_of_exclusive_field_sets, check_fields_exclusive
from vmngclient.model.policy.policy_definition import ListReference, PolicyDefinitionHeader, VariableName


class SequenceIPType(str, Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"


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

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        check_any_of_exclusive_field_sets(
            values,
            [
                ({"data_prefix", "data_prefix_list"}, False),
                ({"fqdn", "fqdn_list"}, False),
                ({"geo_location", "geo_location_list"}, False),
                ({"port", "port_list"}, False),
            ],
        )
        return values


class SecurityGroupIPv6Definition(BaseModel):
    data_ipv6_prefix: Union[IPv6Network, VariableName, None] = Field(None, alias="dataIPV6Prefix")
    data_ipv6_prefix_list: Optional[ListReference] = Field(None, alias="dataIPV6PrefixList")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        check_fields_exclusive(values, {"data_ipv6_prefix", "data_ipv6_prefix_list"}, True)
        return values


class SecurityGroup(PolicyDefinitionHeader):
    # TODO: cannot use sequence_ip_type discriminated unions here as this is root of model
    # EndpointAPI would need to support annotated union as payload parameter
    type: str = Field(default="securityGroup", const=True)
    mode: str = Field(default="unified", const=True)
    sequence_ip_type: SequenceIPType = Field(alias="sequenceIpType")
    definition: Union[SecurityGroupIPv4Definition, SecurityGroupIPv6Definition]

    @root_validator  # type: ignore[call-overload]
    def validate_by_sequence_ip_type(cls, values):
        ip_type = values.get("sequence_ip_type")
        definition = values.get("definition")
        if (ip_type == SequenceIPType.IPV4 and isinstance(definition, SecurityGroupIPv6Definition)) or (
            ip_type == SequenceIPType.IPV6 and isinstance(definition, SecurityGroupIPv4Definition)
        ):
            raise ValueError(f"Incompatible definition for {ip_type} sequence")
        return values
