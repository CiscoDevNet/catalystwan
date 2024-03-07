# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum


class PrintColors(Enum):
    RED_BACKGROUND: str = "\033[41m"
    RED: str = "\033[31m"
    YELLOW: str = "\033[33m"
    BLUE: str = "\033[34m"
    GREEN: str = "\033[32m"
    NONE: str = "\033[0m"
