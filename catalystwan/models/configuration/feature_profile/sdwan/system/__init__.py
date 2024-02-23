from typing import List, Mapping, Union

from .aaa import AAA
from .bfd import BFD

SYSTEM_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
    AAA: "aaa",
    BFD: "bfd",
}

AnySystemParcel = Union[AAA, BFD]

__all__ = ["AAA", "BFD", "AnySystemParcel", "SYSTEM_PAYLOAD_ENDPOINT_MAPPING"]


def __dir__() -> "List[str]":
    return list(__all__)
