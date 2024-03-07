# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pydantic import BaseModel


class DeviceVariable(BaseModel):
    name: str
