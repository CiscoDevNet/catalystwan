# Copyright 2022 Cisco Systems, Inc. and its affiliates

from enum import Enum


class ValidateStatus(Enum):
    validate = "valid"
    invalidate = "invalid"
