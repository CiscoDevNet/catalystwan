# mypy: disable-error-code="empty-body"
from enum import Enum
from ipaddress import IPv4Network, IPv6Network
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, root_validator

from vmngclient.model.policy.policy_definition import PolicyDefinitionHeader


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

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        if values.get("data_prefix") is not None and values.get("data_prefix_list") is not None:
            raise ValueError("geo_location and data_prefix_list cannot be set at the same time")
        if values.get("fqdn") is not None and values.get("fqdn_list") is not None:
            raise ValueError("fqdn and fqdn_list cannot be set at the same time")
        if values.get("geo_location") is not None and values.get("geo_location_list") is not None:
            raise ValueError("geoLocation and geo_location_list cannot be set at the same time")
        if values.get("port") is not None and values.get("port_list") is not None:
            raise ValueError("port and port_list cannot be set at the same time")
        return values


class SecurityGroupIPv6Definition(BaseModel):
    data_ipv6_prefix: Union[IPv6Network, VariableName, None] = Field(None, alias="dataIPV6Prefix")
    data_ipv6_prefix_list: Optional[ListReference] = Field(None, alias="dataIPV6PrefixList")

    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True

    @root_validator  # type: ignore[call-overload]
    def check_exclusive_fields(cls, values):
        if values.get("data_ipv6_prefix") is not None and values.get("data_ipv6_prefix_list") is not None:
            raise ValueError("data_ipv6_prefix and data_ipv6_prefix_list cannot be set at the same time")
        return values


class SecurityGroup(PolicyDefinitionHeader):
    type: str = Field(default="securityGroup", const=True)
    mode: str = Field(default="unified", const=True)


class SecurityGroupDefinition(SecurityGroup):
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
