from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable


class VirtualApplicationType(str, Enum):
    DREOPT = "dreopt"


class ResourceProfile(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra-large"
    DEFAULT = "default"


class VirtualApplication(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    instance_id: Global[int] = Field(default=Global(value=1), alias="instanceId")
    application_type: Global[VirtualApplicationType] = Field(
        default=Global[VirtualApplicationType](value=VirtualApplicationType.DREOPT), alias="applicationType"
    )
    resource_profile: Union[Global[ResourceProfile], Default[str]] = Field(
        default=Global[ResourceProfile](value=ResourceProfile.DEFAULT), alias="resourceProfile"
    )


class AppqoeDeviceRole(str, Enum):
    FORWARDER = "forwarder"
    FORWARDER_AND_SERVICE_NODE = "forwarderAndServiceNode"
    SERVICE_NODE = "serviceNode"
    SERVICE_NODE_WITH_DRE = "serviceNodeWithDre"
    FORWARDER_AND_SERVICE_NODE_WITH_DRE = "forwarderAndServiceNodeWithDre"


class AppnavControllerGroupName(str, Enum):
    ACG_APPQOE = "ACG-APPQOE"


class ServiceNodeGroupName(str, Enum):
    SNG_APPQOE = "SNG-APPQOE"


class Appqoe(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Default[str] = Default(value="/1")
    appnav_controller_group: Global[AppnavControllerGroupName] = Field(
        default=Global[AppnavControllerGroupName](value=AppnavControllerGroupName.ACG_APPQOE),
        alias="appnavControllerGroup",
    )
    service_node_group: Global[ServiceNodeGroupName] = Field(
        default=Global[ServiceNodeGroupName](value=ServiceNodeGroupName.SNG_APPQOE), alias="serviceNodeGroup"
    )
    service_node_groups: List[Global[ServiceNodeGroupName]] = Field(
        default=[Global[ServiceNodeGroupName](value=ServiceNodeGroupName.SNG_APPQOE)], alias="serviceNodeGroups"
    )
    enable: Global[bool] = Global[bool](value=True)
    vpn: Union[Global[int], Default[None], Variable] = Field(default=Global[int](value=0))


class ServiceContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    appqoe: List[Appqoe]


# Frowarder


class ServiceNodeInformation(BaseModel):
    address: Global[str]


class ForwarderController(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable]
    vpn: Global[int] = Global[int](value=1)


class ForwarderAppnavControllerGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_name: Default[AppnavControllerGroupName] = Field(
        default=Default(value=AppnavControllerGroupName.ACG_APPQOE), alias="groupName"
    )
    appnav_controllers: List[ForwarderController] = Field(alias="appnavControllers")


class ForwarderNodeGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Union[Global[str], Default[ServiceNodeGroupName]]
    internal: Default[bool] = Default[bool](value=False)
    service_node: List[ServiceNodeInformation] = Field(alias="serviceNode")


class ForwarderRole(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    appnav_controller_group: List[ForwarderAppnavControllerGroup] = Field(alias="appnavControllerGroup")
    service_node_group: List[ForwarderNodeGroup] = Field(alias="serviceNodeGroup")
    service_context: ServiceContext = Field(alias="serviceContext")


# Forwarder and Service


class ForwarderAndServiceNodeAddress(str, Enum):
    ADDRESS_192_168_2_2 = "192.168.2.2"


class ServiceNodeInformationDefault(BaseModel):
    address: Default[ForwarderAndServiceNodeAddress] = Default[ForwarderAndServiceNodeAddress](
        value=ForwarderAndServiceNodeAddress.ADDRESS_192_168_2_2
    )


class ForwarderAndServiceNodeControllerAddress(str, Enum):
    ADDRESS_192_168_2_1 = "192.168.2.1"


class ForwarderAndServiceNodeController(BaseModel):
    address: Default[ForwarderAndServiceNodeControllerAddress] = Default[ForwarderAndServiceNodeControllerAddress](
        value=ForwarderAndServiceNodeControllerAddress.ADDRESS_192_168_2_1
    )


class ForwarderAndServiceNodeAppnavControllerGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_name: Default[AppnavControllerGroupName] = Field(
        default=Default[AppnavControllerGroupName](value=AppnavControllerGroupName.ACG_APPQOE), alias="groupName"
    )
    appnav_controllers: List[ForwarderAndServiceNodeController] = Field(alias="appnavControllers")


class ForwarderAndServiceNodeGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Default[ServiceNodeGroupName] = Default[ServiceNodeGroupName](value=ServiceNodeGroupName.SNG_APPQOE)
    internal: Default[bool] = Default[bool](value=True)
    service_node: List[ServiceNodeInformationDefault] = Field(alias="serviceNode")


class ForwarderAndServiceNodeRole(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    appnav_controller_group: List[ForwarderAndServiceNodeAppnavControllerGroup] = Field(alias="appnavControllerGroup")
    service_node_group: List[ForwarderAndServiceNodeGroup] = Field(alias="serviceNodeGroup")

    service_context: ServiceContext = Field(alias="serviceContext")


# Service
class ServiceNodeExternalAddress(str, Enum):
    ADDRESS_192_168_2_2 = "192.168.2.2"


class ServiceNodeExternalVpgIp(str, Enum):
    ADDRESS_192_168_2_1 = "192.168.2.1/24"


class ServiceNodeInformationExternal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Default[ServiceNodeExternalAddress] = Default[ServiceNodeExternalAddress](
        value=ServiceNodeExternalAddress.ADDRESS_192_168_2_2
    )
    vpg_ip: Default[ServiceNodeExternalVpgIp] = Field(
        default=Default[ServiceNodeExternalVpgIp](value=ServiceNodeExternalVpgIp.ADDRESS_192_168_2_1), alias="vpgIp"
    )


class ServiceNodeGroup(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Default[ServiceNodeGroupName] = Default[ServiceNodeGroupName](value=ServiceNodeGroupName.SNG_APPQOE)
    external_node: Default[bool] = Field(default=Default[bool](value=True), alias="externalNode")
    service_node: List[ServiceNodeInformationExternal] = Field(
        default=[ServiceNodeInformationExternal()], alias="serviceNode"
    )


class ServiceNodeRole(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    service_node_group: List[ServiceNodeGroup] = Field(default=[ServiceNodeGroup()], alias="serviceNodeGroup")


class AppqoeData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dreopt: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=False)
    virtual_application: Optional[List[VirtualApplication]] = Field(alias="virtualApplication")
    appqoe_device_role: Global[str] = Field(default=Global(value=AppqoeDeviceRole.FORWARDER), alias="appqoeDeviceRole")

    forwarder: Optional[ForwarderRole]
    forwarder_and_service_node: Optional[ForwarderAndServiceNodeRole] = Field(alias="forwarderAndServiceNode")
    service_node: Optional[ServiceNodeRole] = Field(alias="serviceNode")


class AppqoeCreationPayload(BaseModel):
    name: str
    description: Optional[str] = None
    data: AppqoeData
    metadata: Optional[dict] = None
