"""
Modified defaults for endpoint payload usage to reduce boilerplate in model definitions.
Just import BaseModel, Field from here instead pydantic module directly
"""
from functools import wraps
from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict
from pydantic import Field as _Field
from pydantic_core import PydanticUndefined


def common_field(func):
    """
    Decorator for `pydantic.Field` function.
    `alias` keyword argument is replaced by `serialization_alias` and `validation_alias`
    This way we can use non-aliased field name in constructor (together with populate_by_name)
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
