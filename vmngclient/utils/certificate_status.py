from enum import Enum


class CertificateStatus(Enum):
    generated = "tokengenerated"
    installed = "certinstalled"


class ValidityPeriod(str, Enum):
    ONE_YEAR = "1Y"
    TWO_YEARS = "2Y"
