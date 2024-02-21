from typing import List, Mapping

from .aaa import AAA
from .bfd import BFD

SYSTEM_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
    AAA: "aaa",
    BFD: "bfd",
}

__all__ = ["AAA", "BFD"]


def __dir__() -> "List[str]":
    return list(__all__)
