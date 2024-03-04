# Copyright 2022 Cisco Systems, Inc. and its affiliates

from enum import Enum


class Reachability(str, Enum):
    REACHABLE = "reachable"
    UNREACHABLE = "unreachable"
