from enum import Enum


class PrintColors(Enum):
    RED_BACKGROUND: str = "\033[41m"
    RED: str = "\033[31m"
    YELLOW: str = "\033[33m"
    NONE: str = "\033[0m"
