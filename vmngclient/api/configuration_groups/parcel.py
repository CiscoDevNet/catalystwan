from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic.v1 import BaseModel, Extra, Field
from pydantic.v1.generics import GenericModel

T = TypeVar("T")


class Parcel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        extra = Extra.forbid


class OptionType(str, Enum):
    GLOBAL = "global"
    DEFAULT = "default"
    VARIABLE = "variable"


class ParcelValue(BaseModel):
    class Config:
        extra = "forbid"

    optionType: OptionType


class Global(GenericModel, Generic[T], ParcelValue):
    optionType: OptionType = OptionType.GLOBAL
    value: T


class Variable(GenericModel, ParcelValue):
    optionType: OptionType = OptionType.VARIABLE
    value: str


class Default(GenericModel, Generic[T], ParcelValue):
    optionType: OptionType = OptionType.DEFAULT
    value: Any


class MainParcel(BaseModel):
    # TODO add constr or Annotated[constr] in Pydantic v2
    # F722 syntax error in forward annotation
    # https://github.com/pydantic/pydantic/issues/2872
    # https://github.com/pydantic/pydantic/issues/156
    name: str = Field(regex=r'^[^&<>! "]+$', min_length=1, max_length=128)
    description: Optional[str]
    data: Parcel
