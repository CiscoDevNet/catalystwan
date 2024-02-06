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

    mac_address: Union[Global[str], Variable] = Field(alias="macAddress")
    ip: Union[Global[str], Variable]


class DhcpAddressPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    network_address: Union[Global[str], Variable] = Field(alias="networkAddress")
    subnet_mask: Union[Global[str], Variable] = Field(alias="subnetMask")


class DhcpServerData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address_pool: DhcpAddressPool = Field(alias="addressPool")
    exclude: Optional[Union[Global[List[str]], Variable, Default[None]]] = None
    lease_time: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="leaseTime", default=Default[int](value=86400)
    )
    interface_mtu: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="interfaceMtu", default=None)
    domain_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="domainName", default=None)
    default_gateway: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="defaultGateway", default=None)
    dns_servers: Optional[Union[Global[List[str]], Variable, Default[None]]] = Field(alias="dnsServers", default=None)
    tftp_servers: Optional[Union[Global[List[str]], Variable, Default[None]]] = Field(alias="tftpServers", default=None)
    static_lease: Optional[List[StaticLease]] = Field(alias="staticLease", default=None)
    option_code: Optional[List[Union[OptionCodeAscii, OptionCodeHex, OptionCodeIP]]] = Field(
        alias="optionCode", default=None
    )


class DhcpSeverCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: DhcpServerData
    metadata: Optional[dict] = None
