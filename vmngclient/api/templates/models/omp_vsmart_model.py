from pathlib import Path
from typing import ClassVar, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


class OMPvSmart(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    graceful_restart: Optional[bool] = Field(default=None, alias="graceful-restart")
    send_path_limit: Optional[int] = Field(default=None, alias="send-path-limit")
    send_backup_paths: Optional[bool] = Field(default=None, alias="send-backup-paths")
    discard_rejected: Optional[bool] = Field(default=None, alias="discard-rejected")
    shutdown: Optional[bool] = Field(default=None, alias="shutdown")
    graceful_restart_timer: Optional[int] = Field(default=None, alias="graceful-restart-timer", data_path=["timers"])
    eor_timer: Optional[int] = Field(default=None, alias="eor-timer", data_path=["timers"])
    holdtime: Optional[int] = Field(default=None, alias="holdtime", data_path=["timers"])
    affinity_group_preference: Optional[bool] = Field(default=None, alias="affinity-group-preference")
    advertisement_interval: Optional[int] = Field(default=None, alias="advertisement-interval", data_path=["timers"])

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "omp-vsmart"
