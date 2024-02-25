from typing import List, Mapping, Union

from .aaa import AAAParcel
from .bfd import BFDParcel

SYSTEM_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
    AAAParcel: "aaa",
    BFDParcel: "bfd",
}

AnySystemParcel = Union[AAAParcel, BFDParcel]

__all__ = ["AAAParcel", "BFDParcel", "AnySystemParcel", "SYSTEM_PAYLOAD_ENDPOINT_MAPPING"]


def __dir__() -> "List[str]":
    return list(__all__)
