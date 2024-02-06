from enum import Enum

from pydantic import BaseModel, Extra, Field

from catalystwan.models.profileparcel.traffic_policy import GlobalOptionTypeDef, UuidDef


class Solution(str, Enum):
    MOBILITY = "mobility"
    SDWAN = "sdwan"
    NFVIRTUAL = "nfvirtual"
    SDROUTING = "sd-routing"


class RefId(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: UuidDef
