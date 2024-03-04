# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum, auto


class SessionType(Enum):
    SINGLE_TENANT = auto()
    PROVIDER = auto()
    TENANT = auto()
    PROVIDER_AS_TENANT = auto()
    NOT_DEFINED = auto()


ProviderView = SessionType.PROVIDER
TenantView = SessionType.TENANT
ProviderAsTenantView = SessionType.PROVIDER_AS_TENANT
SingleTenantView = SessionType.SINGLE_TENANT
