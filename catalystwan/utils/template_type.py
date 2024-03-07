# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum


class TemplateType(Enum):
    CLI = "file"
    FEATURE = "template"
