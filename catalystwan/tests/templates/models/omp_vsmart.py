# Copyright 2023 Cisco Systems, Inc. and its affiliates

#  type: ignore
from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.models.omp_vsmart_model import OMPvSmart
from catalystwan.utils.device_model import DeviceModel

default_omp = OMPvSmart(template_name="omp_1", template_description="default", device_models=[DeviceModel.VEDGE_C8000V])


omp_2 = OMPvSmart(
    template_name="omp_2",
    template_description="some changes",
    device_models=[DeviceModel.VEDGE_C8000V],
    graceful_restart=False,
    send_backup_paths=False,
    shutdown=True,
    holdtime=30,
)

omp_3 = OMPvSmart(
    template_name="omp_3",
    template_description="advanced",
    device_models=[DeviceModel.VEDGE_C8000V],
    graceful_restart=False,
    graceful_restart_timer=DeviceVariable(name="omp_graceful_restart_timer"),
    send_path_limit=DeviceVariable(name="omp_send_path_limit"),
    discard_rejected=DeviceVariable(name="omp_discard_rejected_custom"),
    send_backup_paths=True,
    shutdown=False,
    advertisement_interval=3,
    holdtime=30,
)
