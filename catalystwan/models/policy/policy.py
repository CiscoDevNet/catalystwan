# Copyright 2023 Cisco Systems, Inc. and its affiliates

import datetime
from typing import List, Literal, Optional, Sequence, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PolicyId(BaseModel):
    policy_id: UUID = Field(serialization_alias="policyId", validation_alias="policyId")


class NGFirewallZoneListEntry(BaseModel):
    src_zone_list_id: UUID = Field(serialization_alias="srcZoneListId", validation_alias="srcZoneListId")
    dst_zone_list_id: UUID = Field(serialization_alias="dstZoneListId", validation_alias="dstZoneListId")
    model_config = ConfigDict(populate_by_name=True)


class AssemblyItemBase(BaseModel):
    definition_id: UUID = Field(serialization_alias="definitionId", validation_alias="definitionId")
    type: str
    model_config = ConfigDict(populate_by_name=True)


class ZoneBasedFWAssemblyItem(AssemblyItemBase):
    type: Literal["zoneBasedFW"] = "zoneBasedFW"


class NGFirewallAssemblyItem(AssemblyItemBase):
    type: Literal["zoneBasedFW"] = "zoneBasedFW"
    entries: List[NGFirewallZoneListEntry] = []

    def add_zone_pair(self, src_zone_id: UUID, dst_zone_id: UUID):
        self.entries.append(NGFirewallZoneListEntry(src_zone_list_id=src_zone_id, dst_zone_list_id=dst_zone_id))


class DNSSecurityAssemblyItem(AssemblyItemBase):
    type: Literal["DNSSecurity"] = "DNSSecurity"


class IntrusionPreventionAssemblyItem(AssemblyItemBase):
    type: Literal["intrusionPrevention"] = "intrusionPrevention"


class URLFilteringAssemblyItem(AssemblyItemBase):
    type: Literal["urlFiltering"] = "urlFiltering"


class AdvancedInspectionProfileAssemblyItem(AssemblyItemBase):
    type: Literal["advancedInspectionProfile"] = "advancedInspectionProfile"


class AdvancedMalwareProtectionAssemblyItem(AssemblyItemBase):
    type: Literal["advancedMalwareProtection"] = "advancedMalwareProtection"


class SSLDecryptionAssemblyItem(AssemblyItemBase):
    type: Literal["sslDecryption"] = "sslDecryption"


class PolicyDefinition(BaseModel):
    assembly: Sequence[AssemblyItemBase] = []


class PolicyCreationPayload(BaseModel):
    policy_name: str = Field(
        serialization_alias="policyName",
        validation_alias="policyName",
        pattern="^[a-zA-Z0-9_-]{1,127}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 127 characters",
    )
    policy_description: str = Field(
        default="default description", serialization_alias="policyDescription", validation_alias="policyDescription"
    )
    policy_type: str = Field(serialization_alias="policyType", validation_alias="policyType")
    policy_definition: Union[PolicyDefinition, str] = Field(
        serialization_alias="policyDefinition", validation_alias="policyDefinition"
    )
    is_policy_activated: bool = Field(
        default=False, serialization_alias="isPolicyActivated", validation_alias="isPolicyActivated"
    )
    model_config = ConfigDict(populate_by_name=True)


class PolicyEditPayload(PolicyCreationPayload, PolicyId):
    pass


class PolicyInfo(PolicyEditPayload):
    created_by: str = Field(serialization_alias="createdBy", validation_alias="createdBy")
    created_on: datetime.datetime = Field(serialization_alias="createdOn", validation_alias="createdOn")
    last_updated_by: str = Field(serialization_alias="lastUpdatedBy", validation_alias="lastUpdatedBy")
    last_updated_on: datetime.datetime = Field(serialization_alias="lastUpdatedOn", validation_alias="lastUpdatedOn")
    policy_version: Optional[str] = Field(None, serialization_alias="policyVersion", validation_alias="policyVersion")


class PolicyPreview(BaseModel):
    preview: str
