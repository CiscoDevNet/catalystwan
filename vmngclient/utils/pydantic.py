"""
Modified defaults for endpoint payload models to reduce boilerplate in model definitions.
Supports pydantic V2 only (and used to ease the migration from V1)
Just import BaseModel, Field from here instead pydantic module directly
"""
from functools import wraps
from typing import Any, Callable, TypeVar

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict
from pydantic import Field as _Field

F = TypeVar("F", bound=Callable)


def common_field(func: F) -> F:
    """
    Decorator for `pydantic.Field` function.
    `alias` keyword argument is replaced by `serialization_alias` and `validation_alias`
    This way we can use non-aliased field name in constructor (together with populate_by_name)
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        _kwargs = dict(kwargs)
        if (alias := _kwargs.pop("alias", None)) is not None:
            _kwargs["serialization_alias"] = alias
            _kwargs["validation_alias"] = alias
        return func(*args, **_kwargs)

    return wrapper  # type: ignore


Field = common_field(_Field)


class BaseModel(_BaseModel):
    model_config = ConfigDict(populate_by_name=True)
