from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class ProtocolListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    protocol: Global[str] = Field(serialization_alias="protocolName", validation_alias="protocolName")


class ProtocolListParcel(_ParcelBase):
    entries: List[ProtocolListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_protocol(self, protocol: str):
        self.entries.append(ProtocolListEntry(protocol=as_global(protocol)))
