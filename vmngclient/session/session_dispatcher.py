from enum import Enum
from typing import Any

from vmngclient.session.session_base import Session, ProviderSession, ProviderAsTenantSession, TenantSession
from vmngclient.utils.creation_tools import get_logger_name


class VmngSessionType(Enum):
    Provider = ProviderSession
    ProviderAsTenant = ProviderAsTenantSession
    Tenant = TenantSession


def SessionHandler(session_type: VmngSessionType, **kwargs: Any) -> Session:
    """Factory function that creates session object based on VmngSessionType."""
    SessionClass = session_type.value
    try:
        return SessionClass(**kwargs)
    except TypeError as e:
        raise TypeError(f"Wrong session parameters for {session_type.value} session: {e}")
    except Exception as e:
        raise Exception(f"Failed to create {session_type.value} session: {e}")
