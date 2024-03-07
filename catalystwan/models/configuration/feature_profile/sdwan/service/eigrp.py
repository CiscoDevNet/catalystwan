# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.feature_profile.common import Prefix

EigrpAuthType = Literal[
    "md5",
    "hmac-sha-256",
]


RedistributeProtocol = Literal[
    "bgp",
    "connected",
    "nat-route",
    "omp",
    "ospf",
    "ospfv3",
    "static",
]


class KeychainDetails(BaseModel):
    key_id: Union[Global[int], Variable, Default[None]] = Field(serialization_alias="keyId", validation_alias="keyId")
    keystring: Union[Global[str], Variable, Default[None]]


class EigrpAuthentication(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    auth_type: Union[Global[EigrpAuthType], Variable, Default[None]] = Field(
        serialization_alias="type", validation_alias="type"
    )
    auth_key: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="authKey", validation_alias="authKey"
    )
    key: Optional[List[KeychainDetails]] = Field(serialization_alias="key", validation_alias="key")


class TableMap(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Optional[Union[Default[None], Global[UUID]]] = Default[None](value=None)
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)


class SummaryAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix


class IPv4StaticRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Union[Global[str], Variable]
    shutdown: Optional[Union[Global[int], Variable, Default[bool]]] = Default[bool](value=False)
    summary_address: Optional[List[SummaryAddress]] = Field(
        serialization_alias="summaryAddress", validation_alias="summaryAddress"
    )


class RedistributeIntoEigrp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocol], Variable]
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Default[None](value=None)


class AddressFamily(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    redistribute: Optional[List[RedistributeIntoEigrp]] = None
    network: List[SummaryAddress]


class EigrpData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    as_number: Union[Global[int], Variable] = Field(serialization_alias="asNum", validation_alias="asNum")
    address_family: AddressFamily = Field(serialization_alias="addressFamily", validation_alias="addressFamily")
    hello_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="helloInterval", validation_alias="helloInterval", default=Default[int](value=5)
    )
    hold_time: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="holdTime", validation_alias="holdTime", default=Default[int](value=15)
    )
    authentication: Optional[EigrpAuthentication] = None
    af_interface: Optional[List[IPv4StaticRoute]] = Field(
        serialization_alias="afInterface", validation_alias="afInterface", default=None
    )
    table_map: TableMap = Field(serialization_alias="tableMap", validation_alias="tableMap", default=TableMap())


class EigrpCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: EigrpData
    metadata: Optional[dict] = None
