# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import TLOCColor
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ColorDSCPMap(BaseModel):
    color: TLOCColor
    dscp: int = Field(ge=0, le=63)


class AppProbeClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    forwarding_class: str = Field(serialization_alias="forwardingClass", validation_alias="forwardingClass")
    map: List[ColorDSCPMap] = []

    def add_color_mapping(self, color: TLOCColor, dscp: int) -> None:
        self.map.append(ColorDSCPMap(color=color, dscp=dscp))


class AppProbeClassList(PolicyListBase):
    type: Literal["appProbe"] = "appProbe"
    entries: List[AppProbeClassListEntry] = []

    def assign_forwarding_class(self, name: str) -> AppProbeClassListEntry:
        # App probe class list must have only one entry!
        entry = AppProbeClassListEntry(forwarding_class=name)
        self._add_entry(entry, single=True)
        return entry


class AppProbeClassListEditPayload(AppProbeClassList, PolicyListId):
    pass


class AppProbeClassListInfo(AppProbeClassList, PolicyListInfo):
    pass
