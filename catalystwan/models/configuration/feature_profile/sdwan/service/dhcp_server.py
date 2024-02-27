# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable


class OptionCodeAscii(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    code: Union[Global[int], Variable]
    ascii: Union[Global[str], Variable]


class OptionCodeHex(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    code: Union[Global[int], Variable]
    hex: Union[Global[str], Variable]


class OptionCodeIP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    code: Union[Global[int], Variable]
    ip: Union[Global[List[str]], Variable]


class StaticLease(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    mac_address: Union[Global[str], Variable] = Field(serialization_alias="macAddress", validation_alias="macAddress")
    ip: Union[Global[str], Variable]


class DhcpAddressPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    network_address: Union[Global[str], Variable] = Field(
        serialization_alias="networkAddress", validation_alias="networkAddress"
    )
    subnet_mask: Union[Global[str], Variable] = Field(serialization_alias="subnetMask", validation_alias="subnetMask")


class DhcpServerData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address_pool: DhcpAddressPool = Field(serialization_alias="addressPool", validation_alias="addressPool")
    exclude: Optional[Union[Global[List[str]], Variable, Default[None]]] = None
    lease_time: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="leaseTime", validation_alias="leaseTime", default=Default[int](value=86400)
    )
    interface_mtu: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="interfaceMtu", validation_alias="interfaceMtu", default=None
    )
    domain_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="domainName", validation_alias="domainName", default=None
    )
    default_gateway: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="defaultGateway", validation_alias="defaultGateway", default=None
    )
    dns_servers: Optional[Union[Global[List[str]], Variable, Default[None]]] = Field(
        serialization_alias="dnsServers", validation_alias="dnsServers", default=None
    )
    tftp_servers: Optional[Union[Global[List[str]], Variable, Default[None]]] = Field(
        serialization_alias="tftpServers", validation_alias="tftpServers", default=None
    )
    static_lease: Optional[List[StaticLease]] = Field(
        serialization_alias="staticLease", validation_alias="staticLease", default=None
    )
    option_code: Optional[List[Union[OptionCodeAscii, OptionCodeHex, OptionCodeIP]]] = Field(
        serialization_alias="optionCode", validation_alias="optionCode", default=None
    )


class DhcpSeverCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: DhcpServerData
    metadata: Optional[dict] = None
