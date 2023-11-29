from ipaddress import IPv4Network, IPv6Network
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Annotated

from vmngclient.model.common import check_fields_exclusive
from vmngclient.model.policy.policy_definition import ListReference, PolicyDefinitionHeader, VariableName


class Reference(BaseModel):
    ref: str


class RuleBase(BaseModel):
    rule: str = ""
    order: str = ""
    action: str = "permit"
    source_security_group: Optional[Reference] = Field(alias="sourceSecurityGroup")
    destination_security_group: Optional[Reference] = Field(alias="destinationSecurityGroup")
    protocol: Optional[str]
    protocol_name: Optional[str] = Field(alias="protocolName")
    protocol_name_list: Optional[Reference] = Field(alias="protocolNameList")
    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def check_exclusive_fields(self):
        check_fields_exclusive(self.__dict__, {"protocol", "protocol_name", "protocol_name_list"}, False)
        return self


class IPv4Rule(RuleBase):
    sequence_ip_type: Literal["ipv4"] = Field("ipv4", alias="sequenceIpType")
    source_ip: Union[IPv4Network, VariableName, None] = Field(None, alias="sourceIP")
    source_data_prefix_list: Optional[ListReference] = Field(None, alias="sourceDataPrefixList")
    source_fqdn: Optional[str] = Field(None, alias="sourceFqdn")
    source_fqdn_list: Optional[ListReference] = Field(None, alias="sourceFqdnList")
    source_geo_location: Optional[str] = Field(None, alias="sourceGeoLocation")
    source_geo_location_list: Optional[ListReference] = Field(None, alias="sourceGeoLocationList")
    source_port: Optional[str] = Field(None, alias="sourcePort")
    source_port_list: Optional[ListReference] = Field(None, alias="sourcePortList")
    destination_ip: Union[IPv4Network, VariableName, None] = Field(None, alias="destinationIP")
    destination_data_prefix_list: Optional[ListReference] = Field(None, alias="destinationDataPrefixList")
    destination_fqdn: Optional[str] = Field(None, alias="destinationFqdn")
    destination_fqdn_list: Optional[ListReference] = Field(None, alias="destinationFqdnList")
    destination_geo_location: Optional[str] = Field(None, alias="destinationGeoLocation")
    destination_geo_location_list: Optional[ListReference] = Field(None, alias="destinationGeoLocationList")
    destination_port: Optional[str] = Field(None, alias="destinationPort")
    destination_port_list: Optional[ListReference] = Field(None, alias="destinationPortList")
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
    sequence_ip_type: Literal["ipv6"] = Field("ipv6", alias="sequenceIpType")
    source_ipv6: Union[IPv6Network, VariableName, None] = Field(None, alias="sourceIPV6")
    source_ipv6_data_prefix_list: Optional[ListReference] = Field(None, alias="sourceIPV6DataPrefixList")
    destination_ipv6: Union[IPv6Network, VariableName, None] = Field(None, alias="destinationIPV6")
    destination_ipv6_data_prefix_list: Optional[ListReference] = Field(None, alias="destinationIPV6DataPrefixList")
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


class RuleSet(PolicyDefinitionHeader):
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
        source_security_group_id: Optional[str] = None,
        source_ip: Optional[IPv4Network] = None,
        source_ip_variable: Optional[str] = None,
        source_data_prefix_list_id: Optional[str] = None,
        source_fqdn: Optional[str] = None,
        source_fqdn_list_id: Optional[str] = None,
        source_geo_location: Optional[str] = None,
        source_geo_location_list_id: Optional[str] = None,
        source_port: Optional[str] = None,
        source_port_list_id: Optional[str] = None,
        destination_security_group_id: Optional[str] = None,
        destination_ip: Optional[IPv4Network] = None,
        destination_ip_variable: Optional[str] = None,
        destination_data_prefix_list_id: Optional[str] = None,
        destination_fqdn: Optional[str] = None,
        destination_fqdn_list_id: Optional[str] = None,
        destination_geo_location: Optional[str] = None,
        destination_geo_location_list_id: Optional[str] = None,
        destination_port: Optional[str] = None,
        destination_port_list_id: Optional[str] = None,
        protocols: Optional[List[int]] = None,
        protocol_names: Optional[str] = None,
        protocol_name_list_id: Optional[str] = None,
    ) -> None:
        if source_ip is not None and source_ip_variable is not None:
            raise ValueError("Source IP and variable name cannot be set at the same time")
        if destination_ip is not None and destination_ip_variable is not None:
            raise ValueError("Destination IP and variable name cannot be set at the same time")
        ipv4_rule = IPv4Rule(  # type: ignore[call-arg]
            action=action,
            source_security_group=source_security_group_id,
            source_ip=source_ip or source_ip_variable,
            source_data_prefix_list=source_data_prefix_list_id,
            source_fqdn=source_fqdn,
            source_fqdn_list=source_fqdn_list_id,
            source_geo_location=source_geo_location,
            source_geo_location_list=source_geo_location_list_id,
            source_port=source_port,
            source_port_list=source_port_list_id,
            destination_security_group=destination_security_group_id,
            destination_ip=destination_ip or destination_ip_variable,
            destination_data_prefix_list=destination_data_prefix_list_id,
            destination_fqdn=destination_fqdn,
            destination_fqdn_list=destination_fqdn_list_id,
            destination_geo_location=destination_geo_location,
            destination_geo_location_list=destination_geo_location_list_id,
            destination_port=destination_port,
            destination_port_list=destination_port_list_id,
            protocol=" ".join(str(p) for p in protocols) if protocols else None,
            protocol_name=" ".join(p for p in protocol_names) if protocol_names else None,
            protocol_name_list=protocol_name_list_id,
        )
        self.add(ipv4_rule)
