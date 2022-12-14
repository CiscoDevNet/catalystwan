from enum import Enum


class CertificateStatus(Enum):
    generated = "tokengenerated"
    installed = "certinstalled"
