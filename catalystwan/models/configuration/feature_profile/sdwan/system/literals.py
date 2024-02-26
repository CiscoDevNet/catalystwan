from typing import Literal

Priority = Literal["information", "debugging", "notice", "warn", "error", "critical", "alert", "emergency"]
Version = Literal["TLSv1.1", "TLSv1.2"]
AuthType = Literal["Server", "Mutual"]

SYSTEM_LITERALS = [Priority, Version, AuthType]
