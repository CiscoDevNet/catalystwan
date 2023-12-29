from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.api.configuration_groups.parcel import Default, Global, Variable


class EndpointProtocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class EndpointTcpUdp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Optional[Union[Variable, Global[EndpointProtocol]]] = None
    port: Optional[Union[Variable, Global[int]]] = None


class TrackerType(str, Enum):
    ENDPOINT = "endpoint"


class EndpointTrackerType(str, Enum):
    STATIC_ROUTE = "static-route"


class TrackerData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Union[Variable, Global[str]] = Field(alias="trackerName")
    endpoint_api_url: Optional[Union[Variable, Global[str]]] = Field(alias="endpointApiUrl", default=None)
    endpoint_dns_name: Optional[Union[Variable, Global[str]]] = Field(alias="endpointDnsName", default=None)
    endpoint_ip: Optional[Union[Variable, Global[str]]] = Field(alias="endpointIp", default=None)
    endpoint_tcp_udp: Optional[EndpointTcpUdp] = Field(alias="endpointTcpUdp", default=None)
    interval: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    multiplier: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=3)
    threshold: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=300)
    endpoint_tracker_type: Optional[Union[Global[EndpointTrackerType], Variable, Default[EndpointTrackerType]]] = Field(
        alias="endpointTrackerType", default=Default[EndpointTrackerType](value=EndpointTrackerType.STATIC_ROUTE)
    )
    tracker_type: Optional[Union[Global[TrackerType], Variable, Default[TrackerType]]] = Field(
        alias="trackerType", default=Default[TrackerType](value=TrackerType.ENDPOINT)
    )


class TrackerParcelCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: TrackerData
    metadata: Optional[dict] = None
