from enum import Enum


class Severity(Enum):
    MINOR = "Minor"
    MEDIUM = "Medium"
    MAJOR = "Major"
    CRITICAL = "Critical"


class Viewed(Enum):
    YES = "true"
    NO = "false"
