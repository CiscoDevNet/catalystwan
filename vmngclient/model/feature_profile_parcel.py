from typing import Optional

from pydantic import BaseModel, Field


class FullConfig(BaseModel):
    fullconfig: str


class FullConfigParcel(BaseModel):
    name: str = Field(regex=r'^[^&<>! "]+$', min_length=1, max_length=128)
    description: Optional[str]
    data: FullConfig
