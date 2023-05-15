from pathlib import Path
from typing import ClassVar, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class OMPvSmart(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    graceful_restart: Optional[bool] = Field(default=None, alias="graceful-restart")
    send_path_limit: Optional[int] = Field(default=None, alias="send-path-limit")
    send_backup_paths: Optional[bool] = Field(default=None, alias="send-backup-paths")
    discard_rejected: Optional[bool] = Field(default=None, alias="discard-rejected")
    shutdown: Optional[bool] = Field(default=None, alias="shutdown")
    graceful_restart_timer: Optional[int] = Field(default=None, alias="graceful-restart-timer")
    eor_timer: Optional[int] = Field(default=None, alias="eor-timer")
    holdtime: Optional[int] = Field(default=None, alias="holdtime")
    affinity_group_preference: Optional[bool] = Field(default=None, alias="affinity-group-preference")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "omp-vsmart"
