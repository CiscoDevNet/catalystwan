from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Parcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


class OptionType(str, Enum):
    GLOBAL = "global"
    DEFAULT = "default"
    VARIABLE = "variable"


class ParcelValue(BaseModel):
    model_config = ConfigDict()

    optionType: OptionType


class Global(ParcelValue, Generic[T]):
    optionType: OptionType = OptionType.GLOBAL
    value: T


class Variable(ParcelValue):
    optionType: OptionType = OptionType.VARIABLE
    value: str


class Default(ParcelValue, Generic[T]):
    optionType: OptionType = OptionType.DEFAULT
    value: Any = None


class MainParcel(BaseModel):
    # TODO add constr or Annotated[constr] in Pydantic v2
    # F722 syntax error in forward annotation
    # https://github.com/pydantic/pydantic/issues/2872
    # https://github.com/pydantic/pydantic/issues/156
    name: str = Field(pattern=r'^[^&<>! "]+$', min_length=1, max_length=128)
    description: Optional[str] = None
    data: Parcel
