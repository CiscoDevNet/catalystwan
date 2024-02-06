from enum import Enum


class Reachability(str, Enum):
    REACHABLE = "reachable"
    UNREACHABLE = "unreachable"
