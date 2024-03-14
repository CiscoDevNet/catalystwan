# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network, IPv6Network
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Annotated

from catalystwan.models.common import check_fields_exclusive
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
    VariableName,
)


class RuleBase(BaseModel):
    rule: str = ""
    order: str = ""
    action: str = "permit"
    source_security_group: Optional[Reference] = Field(
        default=None, serialization_alias="sourceSecurityGroup", validation_alias="sourceSecurityGroup"
    )
    destination_security_group: Optional[Reference] = Field(
        default=None, serialization_alias="destinationSecurityGroup", validation_alias="destinationSecurityGroup"
    )
    protocol: Optional[str] = None
    protocol_name: Optional[str] = Field(
        default=None, serialization_alias="protocolName", validation_alias="protocolName"
    )
    protocol_name_list: Optional[Reference] = Field(
        default=None, serialization_alias="protocolNameList", validation_alias="protocolNameList"
    )
    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        check_fields_exclusive(self.__dict__, {"protocol", "protocol_name", "protocol_name_list"}, False)
        return self


class IPv4Rule(RuleBase):
    sequence_ip_type: Literal["ipv4"] = Field(
        default="ipv4", serialization_alias="sequenceIpType", validation_alias="sequenceIpType"
    )
    source_ip: Union[IPv4Network, VariableName, None] = Field(
        default=None, serialization_alias="sourceIP", validation_alias="sourceIP"
    )
    source_data_prefix_list: Optional[Reference] = Field(
        default=None, serialization_alias="sourceDataPrefixList", validation_alias="sourceDataPrefixList"
    )
    source_fqdn: Optional[str] = Field(default=None, serialization_alias="sourceFqdn", validation_alias="sourceFqdn")
    source_fqdn_list: Optional[Reference] = Field(
        default=None, serialization_alias="sourceFqdnList", validation_alias="sourceFqdnList"
    )
    source_geo_location: Optional[str] = Field(
        default=None, serialization_alias="sourceGeoLocation", validation_alias="sourceGeoLocation"
    )
    source_geo_location_list: Optional[Reference] = Field(
        default=None, serialization_alias="sourceGeoLocationList", validation_alias="sourceGeoLocationList"
    )
    source_port: Optional[str] = Field(default=None, serialization_alias="sourcePort", validation_alias="sourcePort")
    source_port_list: Optional[Reference] = Field(
        default=None, serialization_alias="sourcePortList", validation_alias="sourcePortList"
    )
    destination_ip: Union[IPv4Network, VariableName, None] = Field(
        default=None, serialization_alias="destinationIP", validation_alias="destinationIP"
    )
    destination_data_prefix_list: Optional[Reference] = Field(
        default=None, serialization_alias="destinationDataPrefixList", validation_alias="destinationDataPrefixList"
    )
    destination_fqdn: Optional[str] = Field(
        default=None, serialization_alias="destinationFqdn", validation_alias="destinationFqdn"
    )
    destination_fqdn_list: Optional[Reference] = Field(
        default=None, serialization_alias="destinationFqdnList", validation_alias="destinationFqdnList"
    )
    destination_geo_location: Optional[str] = Field(
        default=None, serialization_alias="destinationGeoLocation", validation_alias="destinationGeoLocation"
    )
    destination_geo_location_list: Optional[Reference] = Field(
        default=None, serialization_alias="destinationGeoLocationList", validation_alias="destinationGeoLocationList"
    )
    destination_port: Optional[str] = Field(
        default=None, serialization_alias="destinationPort", validation_alias="destinationPort"
    )
    destination_port_list: Optional[Reference] = Field(
        default=None, serialization_alias="destinationPortList", validation_alias="destinationPortList"
    )
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        check_fields_exclusive(self.__dict__, {"source_security_group", "source_ip", "source_data_prefix_list"}, False)
        check_fields_exclusive(self.__dict__, {"source_security_group", "source_fqdn", "source_fqdn_list"}, False)
        check_fields_exclusive(
            self.__dict__, {"source_security_group", "source_geo_location", "source_geo_location_list"}, False
        )
        check_fields_exclusive(self.__dict__, {"source_security_group", "source_port", "source_port_list"}, False)
        check_fields_exclusive(
            self.__dict__, {"destination_security_group", "destination_ip", "destination_data_prefix_list"}, False
        )
        check_fields_exclusive(
            self.__dict__, {"destination_security_group", "destination_fqdn", "destination_fqdn_list"}, False
        )
        check_fields_exclusive(
            self.__dict__,
            {"destination_security_group", "destination_geo_location", "destination_geo_location_list"},
            False,
        )
        check_fields_exclusive(
            self.__dict__, {"destination_security_group", "destination_port", "destination_port_list"}, False
        )
        return self


class IPv6Rule(RuleBase):
    sequence_ip_type: Literal["ipv6"] = Field(
        default="ipv6", serialization_alias="sequenceIpType", validation_alias="sequenceIpType"
    )
    source_ipv6: Union[IPv6Network, VariableName, None] = Field(
        default=None, serialization_alias="sourceIPV6", validation_alias="sourceIPV6"
    )
    source_ipv6_data_prefix_list: Optional[Reference] = Field(
        default=None, serialization_alias="sourceIPV6DataPrefixList", validation_alias="sourceIPV6DataPrefixList"
    )
    destination_ipv6: Union[IPv6Network, VariableName, None] = Field(
        default=None, serialization_alias="destinationIPV6", validation_alias="destinationIPV6"
    )
    destination_ipv6_data_prefix_list: Optional[Reference] = Field(
        default=None,
        serialization_alias="destinationIPV6DataPrefixList",
        validation_alias="destinationIPV6DataPrefixList",
    )
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        check_fields_exclusive(
            self.__dict__, {"source_security_group", "source_ipv6", "source_ipv6_data_prefix_list"}, False
        )
        check_fields_exclusive(
            self.__dict__,
            {"destination_security_group", "destination_ipv6", "destination_ipv6_data_prefix_list"},
            False,
        )
        return self


Rule = Annotated[Union[IPv4Rule, IPv6Rule], Field(discriminator="sequence_ip_type")]


class RuleSetDefinition(BaseModel):
    rules: List[Rule] = []


class RuleSet(PolicyDefinitionBase):
    type: Literal["ruleSet"] = "ruleSet"
    definition: RuleSetDefinition = RuleSetDefinition()

    def _enumerate_rules(self, from_index: int = 0) -> None:
        """Updates rules entries with appropriate order and rule values.

        Args:
            from_index (int, optional): Only rules after that index in table will be updated. Defaults to 0.
        """
        start_index = from_index
        rule_count = len(self.definition.rules)
        if from_index < 0:
            start_index = rule_count - start_index
        for i in range(start_index, rule_count):
            order = str(i + 1)
            self.definition.rules[i].order = order
            self.definition.rules[i].rule = f"R{order}"

    def pop(self, index: int = -1) -> None:
        """Removes a rule at given index, consecutive rules will be enumarated again.

        Args:
            index (int, optional): Defaults to -1.
        """
        self.definition.rules.pop(index)
        self._enumerate_rules(index)

    def add(self, rule: Rule) -> None:
        """Adds new rule as last in table, order and rule fields will be autogenerated.

        Args:
            rule (Rule)
        """
        insert_index = len(self.definition.rules)
        self.definition.rules.append(rule)
        self._enumerate_rules(insert_index)

    def add_ipv4_rule(
        self,
        action: str = "permit",
        source_security_group_id: Optional[UUID] = None,
        source_ip: Optional[IPv4Network] = None,
        source_ip_variable: Optional[str] = None,
        source_data_prefix_list_id: Optional[UUID] = None,
        source_fqdn: Optional[str] = None,
        source_fqdn_list_id: Optional[UUID] = None,
        source_geo_location: Optional[str] = None,
        source_geo_location_list_id: Optional[UUID] = None,
        source_port: Optional[str] = None,
        source_port_list_id: Optional[UUID] = None,
        destination_security_group_id: Optional[UUID] = None,
        destination_ip: Optional[IPv4Network] = None,
        destination_ip_variable: Optional[str] = None,
        destination_data_prefix_list_id: Optional[UUID] = None,
        destination_fqdn: Optional[str] = None,
        destination_fqdn_list_id: Optional[UUID] = None,
        destination_geo_location: Optional[str] = None,
        destination_geo_location_list_id: Optional[UUID] = None,
        destination_port: Optional[str] = None,
        destination_port_list_id: Optional[UUID] = None,
        protocols: Optional[List[int]] = None,
        protocol_names: Optional[str] = None,
        protocol_name_list_id: Optional[UUID] = None,
    ) -> None:
        if source_ip is not None and source_ip_variable is not None:
            raise ValueError("Source IP and variable name cannot be set at the same time")
        if destination_ip is not None and destination_ip_variable is not None:
            raise ValueError("Destination IP and variable name cannot be set at the same time")
        ipv4_rule = IPv4Rule(
            action=action,
            source_security_group=Reference(ref=source_security_group_id) if source_security_group_id else None,
            source_ip=source_ip or (VariableName(vip_variable_name=source_ip_variable) if source_ip_variable else None),
            source_data_prefix_list=Reference(ref=source_data_prefix_list_id) if source_data_prefix_list_id else None,
            source_fqdn=source_fqdn,
            source_fqdn_list=Reference(ref=source_fqdn_list_id) if source_fqdn_list_id else None,
            source_geo_location=source_geo_location,
            source_geo_location_list=Reference(ref=source_geo_location_list_id)
            if source_geo_location_list_id
            else None,
            source_port=source_port,
            source_port_list=Reference(ref=source_port_list_id) if source_port_list_id else None,
            destination_security_group=Reference(ref=destination_security_group_id)
            if destination_security_group_id
            else None,
            destination_ip=destination_ip
            or (VariableName(vip_variable_name=destination_ip_variable) if destination_ip_variable else None),
            destination_data_prefix_list=Reference(ref=destination_data_prefix_list_id)
            if destination_data_prefix_list_id
            else None,
            destination_fqdn=destination_fqdn,
            destination_fqdn_list=Reference(ref=destination_fqdn_list_id) if destination_fqdn_list_id else None,
            destination_geo_location=destination_geo_location,
            destination_geo_location_list=Reference(ref=destination_geo_location_list_id)
            if destination_geo_location_list_id
            else None,
            destination_port=destination_port,
            destination_port_list=Reference(ref=destination_port_list_id) if destination_port_list_id else None,
            protocol=" ".join(str(p) for p in protocols) if protocols else None,
            protocol_name=" ".join(p for p in protocol_names) if protocol_names else None,
            protocol_name_list=Reference(ref=protocol_name_list_id) if protocol_name_list_id else None,
        )
        self.add(ipv4_rule)


class RuleSetEditPayload(RuleSet, PolicyDefinitionId):
    pass


class RuleSetGetResponse(RuleSet, PolicyDefinitionGetResponse):
    pass
