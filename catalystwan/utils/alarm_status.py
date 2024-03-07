# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum


class Severity(Enum):
    MINOR = "Minor"
    MEDIUM = "Medium"
    MAJOR = "Major"
    CRITICAL = "Critical"
    UNKNOWN = None


class Viewed(Enum):
    YES = "true"
    NO = "false"
