from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

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


# https://github.com/pydantic/pydantic/discussions/6090
# TODO positional arguments
# Usage: Global[str](value="test")
class Global(ParcelValue, Generic[T]):
    optionType: OptionType = OptionType.GLOBAL
    value: T

    def __len__(self) -> int:
        if isinstance(self.value, str):
            return len(self.value)
        return -1

    def __ge__(self, other: Any) -> bool:
        if isinstance(self.value, int):
            return self.value >= other
        return False

    def __le__(self, other: Any) -> bool:
        if isinstance(self.value, int):
            return self.value <= other
        return False


class Variable(ParcelValue):
    optionType: OptionType = OptionType.VARIABLE
    value: str = Field(pattern=r"^\{\{[.\/\[\]a-zA-Z0-9_-]+\}\}$", min_length=1, max_length=64)


class Default(ParcelValue, Generic[T]):
    optionType: OptionType = OptionType.DEFAULT
    value: Any


class DefaultWitoutValue(ParcelValue):
    optionType: OptionType = OptionType.DEFAULT


class MainParcel(BaseModel):
    name: str = Field(min_length=1, max_length=128, pattern=r'^[^&<>! "]+$')
    description: Optional[str] = Field(default=None, description="Set the parcel description")
    data: SerializeAsAny[Parcel]
