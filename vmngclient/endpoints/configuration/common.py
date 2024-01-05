from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SchemaType(str, Enum):
    POST = "post"
    PUT = "put"


class SchemaTypeQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_type: SchemaType = Field(alias="schemaType")


class Solution(str, Enum):
    MOBILITY = "mobility"
    SDWAN = "sdwan"
    NFVIRTUAL = "nfvirtual"
    SDROUTING = "sd-routing"
