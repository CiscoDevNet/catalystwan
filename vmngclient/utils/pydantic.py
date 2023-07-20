from functools import wraps

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict
from pydantic import Field as _Field


def common_field(func):
    @wraps(func)
    def wrapper(**kwargs):
        """
        Wrapper for `pydantic.Field` changes how `alias` argument works
        alias is used only in serialization and validation and does not modify construcrtor signature
        """
        _kwargs = dict(kwargs)
        if alias := _kwargs.pop("alias", None) is not None:
            _kwargs["serialization_alias"] = alias
            _kwargs["validation_alias"] = alias
        return func(_kwargs)

    return wrapper


Field = common_field(_Field)


class BaseModel(_BaseModel):
    model_config = ConfigDict(populate_by_name=True)
