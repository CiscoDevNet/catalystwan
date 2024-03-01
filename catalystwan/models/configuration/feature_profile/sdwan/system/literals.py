from typing import Literal

Priority = Literal["information", "debugging", "notice", "warn", "error", "critical", "alert", "emergency"]
TlsVersion = Literal["TLSv1.1", "TLSv1.2"]
AuthType = Literal["Server", "Mutual"]
CypherSuite = Literal[
    "rsa-aes-cbc-sha2",
    "rsa-aes-gcm-sha2",
    "ecdhe-rsa-aes-gcm-sha2",
    "aes-128-cbc-sha",
    "aes-256-cbc-sha",
    "dhe-aes-cbc-sha2",
    "dhe-aes-gcm-sha2",
    "ecdhe-ecdsa-aes-gcm-sha2",
    "ecdhe-rsa-aes-cbc-sha2",
]

SYSTEM_LITERALS = [Priority, TlsVersion, AuthType, CypherSuite]
