from typing import List, Mapping, Union

from .aaa import AAAParcel
from .bfd import BFDParcel
from .literals import SYSTEM_LITERALS
from .logging_parcel import LoggingParcel

SYSTEM_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
    AAAParcel: "aaa",
    BFDParcel: "bfd",
}

AnySystemParcel = Union[AAAParcel, BFDParcel, LoggingParcel]

__all__ = [
    "AAAParcel",
    "BFDParcel",
    "LoggingParcel",
    "AnySystemParcel",
    "SYSTEM_LITERALS",
    "SYSTEM_PAYLOAD_ENDPOINT_MAPPING",
]


def __dir__() -> "List[str]":
    return list(__all__)
