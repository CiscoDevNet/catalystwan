from typing import List, Mapping, Union

from pydantic import Field
from typing_extensions import Annotated

from .aaa import AAAParcel

AnySystemParcel = Annotated[Union[AAAParcel], Field(discriminator="type")]

SYSTEM_PAYLOAD_ENDPOINT_MAPPING: Mapping[type, str] = {
    AAAParcel: "aaa",
    # BFDParcel: "bfd",
    # LoggingParcel: "logging",
    # BannerParcel: "banner",
    # BasicParcel: "basic",
    # GlobalParcel: "global",
    # NTPParcel: "ntp",
    # MRFParcel: "mrf",
    # OMPParcel: "omp",
    # SecurityParcel: "security",
    # SNMPParcel: "snmp",
}


__all__ = ["AAAParcel", "AnySystemParcel", "SYSTEM_PAYLOAD_ENDPOINT_MAPPING"]


def __dir__() -> "List[str]":
    return list(__all__)
