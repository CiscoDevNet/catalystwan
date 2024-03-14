from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .dhcp_server import LanVpnDhcpServerParcel

AnyServiceParcel = Annotated[
    Union[LanVpnDhcpServerParcel,],  # noqa: E231
    Field(discriminator="type_"),
]

__all__ = [
    "LanVpnDhcpServerParcel",
    "AnyServiceParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
