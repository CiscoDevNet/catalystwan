from enum import Enum
from typing import Any, Dict, Generic, Literal, Optional, TypeVar, get_origin

from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr, model_serializer

T = TypeVar("T")


class _ParcelBase(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, populate_by_name=True)
    parcel_name: str = Field(
        min_length=1,
        max_length=128,
        pattern=r'^[^&<>! "]+$',
        serialization_alias="name",
        validation_alias="name",
    )
    parcel_description: Optional[str] = Field(
        default=None,
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    # data: Optional[Any] = None
    _parcel_data_key: str = PrivateAttr(default="data")

    @model_serializer(mode="wrap", when_used="json")
    def envelope_parcel_data(self, handler) -> Dict[str, Any]:
        model_dict = handler(self)
        model_dict[self._parcel_data_key] = {}
        remove_keys = []

        for key in model_dict.keys():
            field_info = self.model_fields.get(key)
            if field_info and isinstance(field_info.validation_alias, AliasPath):
                aliases = field_info.validation_alias.convert_to_aliases()
                if aliases and aliases[0] == self._parcel_data_key and len(aliases) == 2:
                    model_dict[self._parcel_data_key][aliases[1]] = model_dict[key]
                    remove_keys.append(key)
        for key in remove_keys:
            del model_dict[key]
        return model_dict


class OptionType(str, Enum):
    GLOBAL = "global"
    DEFAULT = "default"
    VARIABLE = "variable"


class ParcelAttribute(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    option_type: OptionType = Field(serialization_alias="optionType", validation_alias="optionType")


# https://github.com/pydantic/pydantic/discussions/6090
# Usage: Global[str](value="test")
class Global(ParcelAttribute, Generic[T]):
    option_type: OptionType = Field(
        default=OptionType.GLOBAL, serialization_alias="optionType", validation_alias="optionType"
    )
    value: T

    def __len__(self) -> int:
        if isinstance(self.value, (str, list)):
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


class Variable(ParcelAttribute):
    option_type: OptionType = Field(
        default=OptionType.VARIABLE, serialization_alias="optionType", validation_alias="optionType"
    )
    value: str = Field(pattern=r"^\{\{[.\/\[\]a-zA-Z0-9_-]+\}\}$", min_length=1, max_length=64)


class Default(ParcelAttribute, Generic[T]):
    option_type: OptionType = Field(
        default=OptionType.DEFAULT, serialization_alias="optionType", validation_alias="optionType"
    )
    value: Any


def as_global(value: Any, generic_alias: Any = None):
    """Produces Global object given only value (type is induced from value)

    Args:
        value (Any): value of Global object to be produced
        generic_alias (Any, optional): specify alias type like Literal. Defaults to None.

    Returns:
        Global[Any]: global option type object
    """
    if generic_alias is None:
        return Global[type(value)](value=value)  # type: ignore
    elif get_origin(generic_alias) is Literal:
        return Global[generic_alias](value=value)  # type: ignore
    TypeError("Inappropriate type for argument generic_alias")


def as_variable(value: str):
    """Produces Variable object from variable name string

    Args:
        value (str): value of Variable object to be produced

    Returns:
        Variable: variable option type object
    """
    return Variable(value=value)


def as_default(value: Any, generic_alias: Any = None):
    """Produces Default object given only value (type is induced from value)

    Args:
        value (Any): value of Default object to be produced
        generic_alias (Any, optional): specify alias type like Literal. Defaults to None.

    Returns:
        Default[Any]: default option type object
    """
    if generic_alias is None:
        return Default[type(value)](value=value)  # type: ignore
    elif get_origin(generic_alias) is Literal:
        return Default[generic_alias](value=value)  # type: ignore
    TypeError("Inappropriate type for argument generic_alias")
