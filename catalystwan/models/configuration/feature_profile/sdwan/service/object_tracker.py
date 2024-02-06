from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId


class ObjectTrackerType(str, Enum):
    INTERFACE = "Interface"
    SIG = "SIG"
    ROUTE = "Route"


class SigTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        alias="objectTrackerType", default=Global[ObjectTrackerType](value=ObjectTrackerType.SIG)
    )


class InterfaceTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        alias="objectTrackerType", default=Global[ObjectTrackerType](value=ObjectTrackerType.INTERFACE)
    )
    interface: Union[Global[str], Variable]


class RouteTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(alias="objectId")
    object_tracker_type: Global[ObjectTrackerType] = Field(
        alias="objectTrackerType", default=Global[ObjectTrackerType](value=ObjectTrackerType.ROUTE)
    )
    route_ip: Union[Global[str], Variable] = Field(alias="routeIp")
    route_mask: Union[Global[str], Variable, Default[str]] = Field(alias="routeMask")
    vpn: Union[Global[int], Variable, Default[None]] = Default[None](value=None)


class ObjectTrackerCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: Union[InterfaceTracker, RouteTracker, SigTracker]


class ObjectTrackerRef(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    tracker_ref: RefId = Field(alias="trackerRef")


class Criteria(str, Enum):
    AND = "and"
    OR = "or"


class ObjectTrackerGroupData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    object_id: Union[Global[int], Variable] = Field(alias="objectId")
    tracker_refs: List[ObjectTrackerRef] = Field(alias="trackerRefs")
    criteria: Union[Global[Criteria], Variable, Default[Criteria]] = Default[Criteria](value=Criteria.OR)


class ObjectTrackerGroupCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: ObjectTrackerGroupData
    metadata: Optional[dict] = None
