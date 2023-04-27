from enum import Enum, auto


class SessionType(Enum):
    PROVIDER = auto()
    TENANT = auto()
    PROVIDER_AS_TENANT = auto()
    NOT_DEFINED = auto()


ProviderView = SessionType.PROVIDER
TenantView = SessionType.TENANT
ProviderAsTenantView = SessionType.PROVIDER_AS_TENANT
