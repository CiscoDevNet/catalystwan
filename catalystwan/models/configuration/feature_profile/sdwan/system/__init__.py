from typing import List, Mapping, Union

from pydantic import Field
from typing_extensions import Annotated

from .aaa import AAAParcel
from .banner import BannerParcel
from .basic import BasicParcel
from .bfd import BFDParcel
from .global_parcel import GlobalParcel
from .logging_parcel import LoggingParcel
from .mrf import MRFParcel
from .ntp import NTPParcel
from .omp import OMPParcel
from .security import SecurityParcel
from .snmp import SNMPParcel

AnySystemParcel = Annotated[
    Union[
        AAAParcel,
        BFDParcel,
        LoggingParcel,
        BannerParcel,
        BasicParcel,
        GlobalParcel,
        NTPParcel,
        MRFParcel,
        OMPParcel,
        SecurityParcel,
        SNMPParcel,
    ],
    Field(discriminator="type"),
]

SYSTEM_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
    AAAParcel: "aaa",
    BFDParcel: "bfd",
    LoggingParcel: "logging",
    BannerParcel: "banner",
    BasicParcel: "basic",
    GlobalParcel: "global",
    NTPParcel: "ntp",
    MRFParcel: "mrf",
    OMPParcel: "omp",
    SecurityParcel: "security",
    SNMPParcel: "snmp",
}


__all__ = [
    "AAAParcel",
    "BFDParcel",
    "LoggingParcel",
    "BannerParcel",
    "BasicParcel",
    "GlobalParcel",
    "NTPParcel",
    "MRFParcel",
    "OMPParcel",
    "SecurityParcel",
    "SNMPParcel",
    "AnySystemParcel",
    "SYSTEM_PAYLOAD_ENDPOINT_MAPPING",
]


def __dir__() -> "List[str]":
    return list(__all__)
