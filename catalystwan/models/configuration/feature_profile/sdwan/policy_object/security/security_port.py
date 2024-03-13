# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class SecurityPortListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port: Global[str] = Field(description="Ex: 1 or 1-10 by range. Range 0 to 65530")

    @field_validator("port")
    @classmethod
    def check_port(cls, port: Global[str]):
        value = port.value
        if value.count("-") == 0:
            assert 0 <= int(value) <= 65530
            return port

        start_port, end_port = value.split("-")
        start = int(start_port)
        end = int(end_port)
        assert 0 <= start <= 65530
        assert 0 <= end <= 65530
        assert start < end
        return port


class SecurityPortParcel(_ParcelBase):
    type_: Literal["security-port"] = Field(default="security-port", exclude=True)
    entries: List[SecurityPortListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def _add_port(self, port: str):
        self.entries.append(SecurityPortListEntry(port=as_global(port)))

    def add_port(self, port: int):
        self._add_port(str(port))

    def add_port_range(self, start_port: int, end_port: int):
        self._add_port(f"{start_port}-{end_port}")
