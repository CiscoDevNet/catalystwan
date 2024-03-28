# Copyright 2022 Cisco Systems, Inc. and its affiliates

import datetime as dt
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TemplateInformation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    last_updated_by: str = Field(serialization_alias="lastUpdatedBy", validation_alias="lastUpdatedBy")
    id: str = Field(serialization_alias="templateId", validation_alias="templateId")
    factory_default: bool = Field(serialization_alias="factoryDefault", validation_alias="factoryDefault")
    name: str = Field(serialization_alias="templateName", validation_alias="templateName")
    devices_attached: int = Field(serialization_alias="devicesAttached", validation_alias="devicesAttached")
    description: str = Field(serialization_alias="templateDescription", validation_alias="templateDescription")
    last_updated_on: dt.datetime = Field(serialization_alias="lastUpdatedOn", validation_alias="lastUpdatedOn")
    resource_group: Optional[str] = Field(
        default=None, serialization_alias="resourceGroup", validation_alias="resourceGroup"
    )


class FeatureTemplateInformation(TemplateInformation):
    model_config = ConfigDict(populate_by_name=True)

    template_type: str = Field(serialization_alias="templateType", validation_alias="templateType")
    device_type: List[str] = Field(serialization_alias="deviceType", validation_alias="deviceType")
    version: str = Field(serialization_alias="templateMinVersion", validation_alias="templateMinVersion")
    template_definiton: Optional[str] = Field(
        default=None, serialization_alias="templateDefinition", validation_alias="templateDefinition"
    )


class DeviceTemplateInformation(TemplateInformation):
    model_config = ConfigDict(populate_by_name=True)

    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    template_class: str = Field(serialization_alias="templateClass", validation_alias="templateClass")
    config_type: str = Field(serialization_alias="configType", validation_alias="configType")
    template_attached: int = Field(serialization_alias="templateAttached", validation_alias="templateAttached")
    draft_mode: Optional[str] = Field(default=None, serialization_alias="draftMode", validation_alias="draftMode")
    device_role: Optional[str] = Field(default=None, serialization_alias="deviceRole", validation_alias="deviceRole")
