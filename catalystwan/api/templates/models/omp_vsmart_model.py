# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate


class OMPvSmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    graceful_restart: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "graceful-restart"})
    send_path_limit: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "send-path-limit"})
    send_backup_paths: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "send-backup-paths"})
    discard_rejected: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "discard-rejected"})
    shutdown: Optional[BoolStr] = Field(default=None, json_schema_extra={"vmanage_key": "shutdown"})
    graceful_restart_timer: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "graceful-restart-timer", "data_path": ["timers"]}
    )
    eor_timer: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "eor-timer", "data_path": ["timers"]}
    )
    holdtime: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "holdtime", "data_path": ["timers"]}
    )
    affinity_group_preference: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "affinity-group-preference"}
    )
    advertisement_interval: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "advertisement-interval", "data_path": ["timers"]}
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "omp-vsmart"
