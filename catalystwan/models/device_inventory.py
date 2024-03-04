# Copyright 2024 Cisco Systems, Inc. and its affiliates

import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BoostrapConfigurationDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bootstrap_config: str = Field(serialization_alias="bootstrapConfig", validation_alias="bootstrapConfig")

    uuid: Optional[UUID] = Field(default=None)
    otp: Optional[str] = Field(default=None)
    vbond: Optional[str] = Field(default=None)
    org: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def try_parse(self):
        matched_groups = re.search(
            r"- uuid : (\S+).*?- otp : (\S+).*?- vbond : (\S+).*?- org : (\S+)", self.bootstrap_config, re.DOTALL
        )
        if matched_groups:
            self.uuid = matched_groups.group(1)
            self.otp = matched_groups.group(2)
            self.vbond = matched_groups.group(3)
            self.org = matched_groups.group(4)
        return self
