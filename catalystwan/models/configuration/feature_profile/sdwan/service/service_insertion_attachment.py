from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable

AttachmentType = Literal[
    "custom",
    "auto",
]

TrafficDirection = Literal[
    "UNIDIR",
    "BIDIR",
]

ReachableInterfaceType = Literal[
    "ipv4",
    "ipv6",
    "tunnel",
]

TrackType = Literal[
    "service-icmp",
    "ipv6-service-icmp",
]

InterfaceType = Literal[
    "fromservice",
    "toservice",
]

RedundancyType = Literal[
    "active",
    "backup",
]

ServiceType = Literal[
    "Firewall",
    "Intrusion-detection",
    "Intrusion-detection-prevention",
    "NETSVC1",
    "NETSVC2",
    "NETSVC3",
    "NETSVC4",
    "NETSVC5",
    "NETSVC6",
    "NETSVC7",
]


class GatewayInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="gatewayInterfaceName", validation_alias="gatewayInterfaceName", default=None
    )
    ip_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="gatewayIpAddress", validation_alias="gatewayIpAddress", default=None
    )
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="gatewayIpv6Address", validation_alias="gatewayIpv6Address", default=None
    )


class ServiceInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="serviceInterfaceName", validation_alias="serviceInterfaceName", default=None
    )
    ip_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="serviceIpAddress", validation_alias="serviceIpAddress", default=None
    )
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="serviceIpv6Address", validation_alias="serviceIpv6Address", default=None
    )


class TrackingIP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ipv4: Optional[Union[Global[str], Variable]] = None
    ipv6: Optional[Union[Global[str], Variable]] = None


class ReachableInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    type: Global[ReachableInterfaceType] = Field(
        serialization_alias="reachableInterfaceType", validation_alias="reachableInterfaceType"
    )
    name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="reachableInterfaceName", validation_alias="reachableInterfaceName"
    )
    ip_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="reachableIpAddress", validation_alias="reachableIpAddress", default=None
    )
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="reachableIpv6Address", validation_alias="reachableIpv6Address", default=None
    )
    tracking_ip: Optional[TrackingIP] = Field(
        serialization_alias="trackingIp", validation_alias="trackingIp", default=None
    )
    track_name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="trackName", validation_alias="trackName", default=None
    )
    track_type: Optional[Union[Global[TrackType], Variable]] = Field(
        serialization_alias="trackType", validation_alias="trackType", default=None
    )


class InterfaceProperties(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    gateway_interface: Optional[GatewayInterface] = Field(
        serialization_alias="gatewayInterface", validation_alias="gatewayInterface", default=None
    )
    service_interface: Optional[ServiceInterface] = Field(
        serialization_alias="serviceInterface", validation_alias="serviceInterface", default=None
    )
    reachable_interface: Optional[ReachableInterface] = Field(
        serialization_alias="reachableInterface", validation_alias="reachableInterface", default=None
    )
    interface_type: Optional[Union[Global[InterfaceType], Variable]] = Field(
        serialization_alias="interfaceType", validation_alias="interfaceType", default=None
    )
    redundancy_type: Optional[Union[Global[RedundancyType], Variable]] = Field(
        serialization_alias="redundancyType", validation_alias="redundancyType", default=None
    )


class Attachment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_properties: List[InterfaceProperties] = Field(
        serialization_alias="interfaceProperties", validation_alias="interfaceProperties"
    )
    traffic_direction: Optional[Union[Global[TrafficDirection], Variable]] = Field(
        serialization_alias="trafficDirection", validation_alias="trafficDirection", default=None
    )


class TrackConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interval: Optional[Union[Global[int], Variable]] = None
    threshold: Optional[Union[Global[int], Variable]] = None
    multiplier: Optional[Union[Global[int], Variable]] = None


class Service(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    service_type: Union[Global[ServiceType], Variable] = Field(
        serialization_alias="serviceType", validation_alias="serviceType"
    )
    default_track: Optional[Union[Global[bool], Default[bool]]] = Field(
        serialization_alias="defaultTrack", validation_alias="defaultTrack", default=None
    )
    track: Optional[Global[bool]] = None
    track_config: Optional[TrackConfig] = Field(
        serialization_alias="trackConfig", validation_alias="trackConfig", default=None
    )
    attachments: Optional[List[Attachment]] = None


class ServiceInsertionAttachmentData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    attachment_type: Optional[Union[Global[AttachmentType], Variable]] = Field(
        serialization_alias="attachmentType", validation_alias="attachmentType", default=None
    )
    service_chain_instance_id: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="serviceChainInstanceID", validation_alias="serviceChainInstanceID", default=None
    )
    service_chain_definition_id: Global[UUID] = Field(
        serialization_alias="serviceChainDefinitionID", validation_alias="serviceChainDefinitionID"
    )
    vpn: Union[Global[int], Variable]
    services: Optional[List[Service]] = None


class ServiceInsertionAttachmentCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: ServiceInsertionAttachmentData
