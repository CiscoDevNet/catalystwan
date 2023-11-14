from pathlib import Path
from typing import ClassVar, Optional

from pydantic.v1 import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


class OMPvSmart(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    graceful_restart: Optional[bool] = Field(default=None, vmanage_key="graceful-restart")
    send_path_limit: Optional[int] = Field(default=None, vmanage_key="send-path-limit")
    send_backup_paths: Optional[bool] = Field(default=None, vmanage_key="send-backup-paths")
    discard_rejected: Optional[bool] = Field(default=None, vmanage_key="discard-rejected")
    shutdown: Optional[bool] = Field(default=None, vmanage_key="shutdown")
    graceful_restart_timer: Optional[int] = Field(
        default=None, vmanage_key="graceful-restart-timer", data_path=["timers"]
    )
    eor_timer: Optional[int] = Field(default=None, vmanage_key="eor-timer", data_path=["timers"])
    holdtime: Optional[int] = Field(default=None, vmanage_key="holdtime", data_path=["timers"])
    affinity_group_preference: Optional[bool] = Field(default=None, vmanage_key="affinity-group-preference")
    advertisement_interval: Optional[int] = Field(
        default=None, vmanage_key="advertisement-interval", data_path=["timers"]
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "omp-vsmart"
