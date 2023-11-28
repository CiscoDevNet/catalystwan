from typing import Any, List

from pydantic.v1 import BaseModel, Field


class FeatureTemplatePayload(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str = Field(alias="templateName")
    description: str = Field(alias="templateDescription")
    template_type: str = Field(alias="templateType")  # Enum
    device_types: List[str] = Field(alias="deviceType")  # Enum
    default: bool = Field(alias="factoryDefault", default=False)
    version: str = Field(alias="templateMinVersion", default="15.0.0")  # Enum
    definition: Any = Field(alias="templateDefinition")
