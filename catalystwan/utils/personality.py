# Copyright 2022 Cisco Systems, Inc. and its affiliates

from enum import Enum


class Personality(str, Enum):
    VSMART = "vsmart"
    VBOND = "vbond"
    EDGE = "vedge"
    VMANAGE = "vmanage"
