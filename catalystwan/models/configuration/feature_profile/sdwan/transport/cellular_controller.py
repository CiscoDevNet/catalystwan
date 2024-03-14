# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

ConfigTypeValue = Literal["non-eSim"]


class ControllerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, populate_by_name=True)
    id: Union[Variable, Global[str]] = Field(min_length=1, max_length=5, description="Cellular ID")
    slot: Union[Variable, Global[int], Default[int], None] = Field(
        default=None, description="Set primary SIM slot", ge=0, le=1
    )
    max_retry: Union[Variable, Global[int], Default[None], None] = Field(
        default=None,
        description="Set SIM failover retries",
        ge=0,
        le=65535,
        serialization_alias="maxRetry",
        validation_alias="maxRetry",
    )
    failover_timer: Union[Variable, Global[int], Default[None], None] = Field(
        default=None,
        description="Set SIM failover timeout in minutes",
        ge=3,
        le=7,
        serialization_alias="failovertimer",
        validation_alias="failovertimer",
    )
    auto_sim: Union[Variable, Global[bool], Default[None], None] = Field(
        default=None,
        description="Enable/Disable Firmware Auto Sim",
        serialization_alias="autoSim",
        validation_alias="autoSim",
    )


class CellularControllerParcel(_ParcelBase):
    type_: Literal["cellular-controller"] = Field(default="cellular-controller", exclude=True)
    config_type: Default[ConfigTypeValue] = Field(
        default=Default(value="non-eSim"), validation_alias=AliasPath("data", "configType")
    )
    controller_config: ControllerConfig = Field(validation_alias=AliasPath("data", "controllerConfig"))

    @staticmethod
    def add_controller_config(
        id: Union[Variable, Global[str]],
        max_retry: Union[Variable, Global[int], Default[None], None] = None,
        failover_timer: Union[Variable, Global[int], Default[None], None] = None,
        auto_sim: Union[Variable, Global[bool], Default[None], None] = None,
    ):
        return ControllerConfig(id=id, max_retry=max_retry, failover_timer=failover_timer, auto_sim=auto_sim)
