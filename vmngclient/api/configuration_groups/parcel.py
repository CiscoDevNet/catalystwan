from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Parcel(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, populate_by_name=True)


class OptionType(str, Enum):
    GLOBAL = "global"
    DEFAULT = "default"
    VARIABLE = "variable"


class ParcelValue(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    optionType: OptionType


class Global(Generic[T], ParcelValue):
    optionType: OptionType = OptionType.GLOBAL
    value: T


# pattern=r'^\{\{[.\/\[\]a-zA-Z0-9_-]+\}\}$', min_length=1, max_length=64
class Variable(ParcelValue):
    optionType: OptionType = OptionType.VARIABLE
    value: str


class Default(Generic[T], ParcelValue):
    optionType: OptionType = OptionType.DEFAULT
    value: Any


class MainParcel(BaseModel):
    # name: Annotated[str, StringConstraints(min_length=1, max_length=128, pattern=r'^[^&<>! "]+$')]
    name: str
    description: Optional[str] = Field(default=None, description="Set the parcel description")
    # data: SerializeAsAny[Parcel]
