# Copyright 2022 Cisco Systems, Inc. and its affiliates

from enum import Enum


class ConfigStatus(Enum):
    sync = "In Sync"
    out_sync = "Out Sync"
