# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .bgp import WanRoutingBgpParcel as BGPParcel
from .cellular_controller import CellularControllerParcel

AnyTransportParcel = Annotated[Union[BGPParcel, CellularControllerParcel], Field(discriminator="type_")]

__all__ = ["BGPParcel", "CellularControllerParcel", "AnyTransportParcel"]


def __dir__() -> "List[str]":
    return list(__all__)
