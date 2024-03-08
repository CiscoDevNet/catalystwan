from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TopologyGroup(BaseModel):
    name: str
    solution: Literal["sdwan"] = "sdwan"
    profiles: List[UUID] = []
    from_topology_group: Optional[UUID] = Field(
        default=None, serialization_alias="fromTopologyGroup", validation_alias="fromTopologyGroup"
    )
