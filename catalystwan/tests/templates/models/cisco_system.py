# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_system import CiscoSystemModel
from catalystwan.utils.device_model import DeviceModel

default_cisco_system = CiscoSystemModel(
    name="default_cisco_system", description="default", device_models=[DeviceModel.VEDGE_C8000V]
)  # type: ignore
