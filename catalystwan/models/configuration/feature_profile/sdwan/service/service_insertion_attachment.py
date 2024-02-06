from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.profileparcel.traffic_policy import RefId


class AttachmentType(str, Enum):
    CUSTOM = "custom"
    AUTO = "auto"


class TrafficDirection(str, Enum):
    UNIDIR = "UNIDIR"
    BIDIR = "BIDIR"


class GatewayInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Optional[Union[Global[str], Variable]] = Field(alias="gatewayInterfaceName", default=None)
    ip_address: Optional[Union[Global[str], Variable]] = Field(alias="gatewayIpAddress", default=None)
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(alias="gatewayIpv6Address", default=None)


class ServiceInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Optional[Union[Global[str], Variable]] = Field(alias="serviceInterfaceName", default=None)
    ip_address: Optional[Union[Global[str], Variable]] = Field(alias="serviceIpAddress", default=None)
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(alias="serviceIpv6Address", default=None)


class ReachableInterfaceType(str, Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    TUNNEL = "tunnel"


class TrackType(str, Enum):
    SERVICE_ICMP = "service-icmp"
    IPV6_SERVICE_ICMP = "ipv6-service-icmp"


class InterfaceType(str, Enum):
    FROM_SERVICE = "fromservice"
    TO_SERVICE = "toservice"


class RedundancyType(str, Enum):
    ACTIVE = "active"
    BACKUP = "backup"


class TrackingIP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ipv4: Optional[Union[Global[str], Variable]] = None
    ipv6: Optional[Union[Global[str], Variable]] = None


class ReachableInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    type: Global[ReachableInterfaceType] = Field(alias="reachableInterfaceType")
    name: Optional[Union[Global[str], Variable]] = Field(alias="reachableInterfaceName")
    ip_address: Optional[Union[Global[str], Variable]] = Field(alias="reachableIpAddress", default=None)
    ipv6_address: Optional[Union[Global[str], Variable]] = Field(alias="reachableIpv6Address", default=None)
    tracking_ip: Optional[TrackingIP] = Field(alias="trackingIp", default=None)
    track_name: Optional[Union[Global[str], Variable]] = Field(alias="trackName", default=None)
    track_type: Optional[Union[Global[TrackType], Variable]] = Field(alias="trackType", default=None)


class InterfaceProperties(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    gateway_interface: Optional[GatewayInterface] = Field(alias="gatewayInterface", default=None)
    service_interface: Optional[ServiceInterface] = Field(alias="serviceInterface", default=None)
    reachable_interface: Optional[ReachableInterface] = Field(alias="reachableInterface", default=None)
    interface_type: Optional[Union[Global[InterfaceType], Variable]] = Field(alias="interfaceType", default=None)
    redundancy_type: Optional[Union[Global[RedundancyType], Variable]] = Field(alias="redundancyType", default=None)


class Attachment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_properties: List[InterfaceProperties] = Field(alias="interfaceProperties")
    traffic_direction: Optional[Union[Global[TrafficDirection], Variable]] = Field(
        alias="trafficDirection", default=None
    )


class TrackConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interval: Optional[Union[Global[int], Variable]] = None
    threshold: Optional[Union[Global[int], Variable]] = None
    multiplier: Optional[Union[Global[int], Variable]] = None


class ServiceType(str, Enum):
    FIREWALL = "Firewall"
    INTRUSION_DETECION = "Intrusion-detection"
    INTRUSION_DETECION_PREVENTION = "Intrusion-detection-prevention"
    NETSVC1 = "NETSVC1"
    NETSVC2 = "NETSVC2"
    NETSVC3 = "NETSVC3"
    NETSVC4 = "NETSVC4"
    NETSVC5 = "NETSVC5"
    NETSVC6 = "NETSVC6"
    NETSVC7 = "NETSVC7"


class Service(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    service_type: Union[Global[ServiceType], Variable] = Field(alias="serviceType")
    default_track: Optional[Union[Global[bool], Default[bool]]] = Field(alias="defaultTrack", default=None)
    track: Optional[Global[bool]] = None
    track_config: Optional[TrackConfig] = Field(alias="trackConfig", default=None)
    attachments: Optional[List[Attachment]] = None


class ServiceInsertionAttachmentData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    attachment_type: Optional[Union[Global[AttachmentType], Variable]] = Field(alias="attachmentType", default=None)
    service_chain_instance_id: Optional[Union[Global[str], Variable]] = Field(
        alias="serviceChainInstanceID", default=None
    )
    service_chain_definition_id: RefId = Field(alias="serviceChainDefinitionID")
    vpn: Union[Global[int], Variable]
    services: Optional[List[Service]] = None


class ServiceInsertionAttachmentCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: ServiceInsertionAttachmentData
