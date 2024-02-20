from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable

ObjectTrackerType = Literal[
    "Interface",
    "SIG",
    "Route",
]


Criteria = Literal[
    "and",
    "or",
]


class SigTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        serialization_alias="objectTrackerType",
        validation_alias="objectTrackerType",
        default=Global[ObjectTrackerType](value="SIG"),
    )


class InterfaceTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        serialization_alias="objectTrackerType",
        validation_alias="objectTrackerType",
        default=Global[ObjectTrackerType](value="Interface"),
    )
    interface: Union[Global[str], Variable]


class RouteTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        serialization_alias="objectTrackerType",
        validation_alias="objectTrackerType",
        default=Global[ObjectTrackerType](value="Route"),
    )
    route_ip: Union[Global[str], Variable] = Field(serialization_alias="routeIp", validation_alias="routeIp")
    route_mask: Union[Global[str], Variable, Default[str]] = Field(
        serialization_alias="routeMask", validation_alias="routeMask"
    )
    vpn: Union[Global[int], Variable, Default[None]] = Default[None](value=None)


class ObjectTrackerCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: Union[InterfaceTracker, RouteTracker, SigTracker]


class ObjectTrackerRef(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tracker_ref: Global[UUID] = Field(serialization_alias="trackerRef", validation_alias="trackerRef")


class ObjectTrackerGroupData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(serialization_alias="objectId", validation_alias="objectId")
    tracker_refs: List[ObjectTrackerRef] = Field(serialization_alias="trackerRefs", validation_alias="trackerRefs")
    criteria: Union[Global[Criteria], Variable, Default[Criteria]] = Default[Criteria](value="or")


class ObjectTrackerGroupCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: ObjectTrackerGroupData
    metadata: Optional[dict] = None
