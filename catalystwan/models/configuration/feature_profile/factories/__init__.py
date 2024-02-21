from typing import Any, Dict, List, Union

from .aaa import AAAFactory
from .bfd import BFDFactory

AnyFactory = Union[AAAFactory, BFDFactory]
supported_parcel_factories: Dict[Any, AnyFactory] = {
    ("cisco_aaa", "cedge_aaa"): AAAFactory,  # type: ignore[dict-item]
    ("cisco_bfd",): BFDFactory,  # type: ignore[dict-item]
}


__all__ = ["AAAFactory", "BFDFactory"]


def __dir__() -> "List[str]":
    return list(__all__)
