from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .thousandeyes import ThousandEyesParcel
from .ucse import UcseParcel

AnyOtherParcel = Annotated[
    Union[ThousandEyesParcel, UcseParcel],  # noqa: #231
    Field(discriminator="type_"),
]

__all__ = [
    "ThousandEyesParcel",
    "UcseParcel",
    "AnyOtherParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
