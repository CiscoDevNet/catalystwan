from pathlib import Path
from typing import ClassVar

from vmngclient.api.templates.feature_template import FeatureTemplate


class CiscoSystemModel(FeatureTemplate):
    hostname: str
    system_ip: str
    site_id: str
    multitenant: bool
    console_baud_rate: int

    class Config:
        arbitrary_types_allowed = True

    payload_path: ClassVar[Path] = Path(__file__).parent / "feature/cisco_system.json.j2"
    type: ClassVar[str] = "cisco_system"  # Cisco System
