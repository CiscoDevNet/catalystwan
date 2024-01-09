from enum import Enum
from typing import Union

from pydantic import Field

from vmngclient.api.configuration_groups.parcel import Default, Global, Parcel, Variable


class ConfigTypeValue(Enum):
    NON_E_SIM = "non-eSim"


class ControllerConfig(Parcel):
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


class CellularController(Parcel):
    config_type: Default[ConfigTypeValue] = Field(
        default=Default(value=ConfigTypeValue.NON_E_SIM),
        serialization_alias="configType",
        validation_alias="configType",
    )
    controller_config: ControllerConfig = Field(alias="controllerConfig")

    @staticmethod
    def add_controller_config(
        id: Union[Variable, Global[str]],
        max_retry: Union[Variable, Global[int], Default[None], None] = None,
        failover_timer: Union[Variable, Global[int], Default[None], None] = None,
        auto_sim: Union[Variable, Global[bool], Default[None], None] = None,
    ):
        return ControllerConfig(id=id, max_retry=max_retry, failover_timer=failover_timer, auto_sim=auto_sim)
