from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .thousandeyes import ThousandEyesParcel

AnyOtherParcel = Annotated[
    Union[ThousandEyesParcel,],  # noqa: #231
    Field(discriminator="type_"),
]

__all__ = [
    "ThousandEyesParcel",
    "AnyOtherParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
