from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId
from catalystwan.models.configuration.feature_profile.common import Prefix


class EigrpAuthType(str, Enum):
    MD5 = "md5"
    HMAC_SHA_256 = "hmac-sha-256"


class KeychainDetails(BaseModel):
    key_id: Union[Global[int], Variable, Default[None]] = Field(alias="keyId")
    keystring: Union[Global[str], Variable, Default[None]]


class EigrpAuthentication(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    auth_type: Union[Global[EigrpAuthType], Variable, Default[None]] = Field(alias="type")
    auth_key: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="authKey")
    key: Optional[List[KeychainDetails]] = Field(alias="key")


class TableMap(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Optional[Union[Default[None], RefId]] = Default[None](value=None)
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)


class SummaryAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix


class IPv4StaticRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Union[Global[str], Variable]
    shutdown: Optional[Union[Global[int], Variable, Default[bool]]] = Default[bool](value=False)
    summary_address: Optional[List[SummaryAddress]] = Field(alias="summaryAddress")


class RedistributeProtocol(str, Enum):
    BGP = "bgp"
    CONNECTED = "connected"
    NAT = "nat-route"
    OMP = "omp"
    OSPF = "ospf"
    OSPFV3 = "ospfv3"
    STATIC = "static"


class RedistributeIntoEigrp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocol], Variable]
    route_policy: Optional[Union[Default[None], RefId]] = Default[None](value=None)


class AddressFamily(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    redistribute: Optional[List[RedistributeIntoEigrp]] = None
    network: List[SummaryAddress]


class EigrpData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    as_number: Union[Global[int], Variable] = Field(alias="asNum")
    address_family: AddressFamily = Field(alias="addressFamily")
    hello_interval: Union[Global[int], Variable, Default[int]] = Field(
        alias="helloInterval", default=Default[int](value=5)
    )
    hold_time: Union[Global[int], Variable, Default[int]] = Field(alias="holdTime", default=Default[int](value=15))
    authentication: Optional[EigrpAuthentication] = None
    af_interface: Optional[List[IPv4StaticRoute]] = Field(alias="afInterface", default=None)
    table_map: TableMap = Field(alias="tableMap", default=TableMap())


class EigrpCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: EigrpData
    metadata: Optional[dict] = None
