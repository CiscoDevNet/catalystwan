# Copyright 2024 Cisco Systems, Inc. and its affiliates

from enum import Enum
from typing import Union

from pydantic import BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase


class ConfigTypeValue(Enum):
    NON_E_SIM = "non-eSim"


class ControllerConfig(BaseModel):
    id: Union[Variable, Global[str]] = Field(min_length=1, max_length=5, description="Cellular ID")
    slot: Union[Variable, Global[int], Default[int], None] = Field(
        default=None, description="Set primary SIM slot", ge=0, le=1
    )
    maxRetry: Union[Variable, Global[int], Default[None], None] = Field(
        default=None, description="Set SIM failover retries", ge=0, le=65535
    )
    failovertimer: Union[Variable, Global[int], Default[None], None] = Field(
        default=None, description="Set SIM failover timeout in minutes", ge=3, le=7
    )
    autoSim: Union[Variable, Global[bool], Default[None], None] = Field(
        default=None, description="Enable/Disable Firmware Auto Sim"
    )


class CellularControllerParcel(_ParcelBase):
    config_type: Default[ConfigTypeValue] = Field(default=Default(value=ConfigTypeValue.NON_E_SIM), alias="configType")
    controller_config: ControllerConfig = Field(alias="controllerConfig")
