# from enum import Enum
# from pathlib import Path
# from typing import ClassVar, List, Optional

# from pydantic import BaseModel, Field

# from vmngclient.api.templates.feature_template import FeatureTemplate

# class CiscoSystemModel(FeatureTemplate):
#     class Config:
#         arbitrary_types_allowed = True
#         allow_population_by_field_name = True

#     admin_tech_on_failure: bool = Field(alias="admin-tech-on-failure")
#     affinity_group_number: bool = Field(alias="admin-tech-on-failure")
#     admin_tech_on_failure: bool = Field(alias="admin-tech-on-failure")
#     admin_tech_on_failure: bool = Field(alias="admin-tech-on-failure")
#     admin_tech_on_failure: bool = Field(alias="admin-tech-on-failure")
#     admin_tech_on_failure: bool = Field(alias="admin-tech-on-failure")
#     admin_tech_on_failure: bool = Field(alias="admin-tech-on-failure")


#     payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
#     type: ClassVar[str] = "cisco_system"
