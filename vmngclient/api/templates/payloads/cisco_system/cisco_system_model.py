# vipType: ignore
from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from attr import define  # type: ignore

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.session import vManageSession


@define
class System:
    host_name: str
    system_ip: str
    site_id: str
    multi_tenant: bool
    console_baud_rate: int


class CiscoSystemModel(FeatureTemplate):
    host_name: str
    system_ip: str
    site_id: str
    multi_tenant: bool
    console_baud_rate: int

    class Config:
        arbitrary_types_allowed = True

    payload_path: ClassVar[Path] = Path(__file__).parent / "feature/cisco_system.json.j2"

    def generate_payload(self, session: vManageSession) -> str:
        return super().generate_payload(session)
