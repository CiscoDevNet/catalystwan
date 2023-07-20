"""
Module which updates pydantic BaseModel and Field
Modified for endpoint payload usage to reduce boilerplate in model definitions
"""
from functools import wraps
from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict
from pydantic import Field as _Field
from pydantic_core import PydanticUndefined


def common_field(func):
    """
    Decorator for `pydantic.Field` function changes how `alias` argument works
    alias is used only in serialization and validation and does not modify construcrtor signature
    """

    @wraps(func)
    def wrapper(default: Any = PydanticUndefined, **kwargs):
        _kwargs = dict(kwargs)
        if (alias := _kwargs.pop("alias", None)) is not None:
            _kwargs["serialization_alias"] = alias
            _kwargs["validation_alias"] = alias
        return func(default, **_kwargs)

    return wrapper


Field = common_field(_Field)


class BaseModel(_BaseModel):
    __doc__ = _BaseModel.__doc__
    model_config = ConfigDict(populate_by_name=True)
