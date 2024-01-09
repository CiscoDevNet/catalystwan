import datetime
from typing import Any, List, Literal, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field


class PolicyId(BaseModel):
    policy_id: str = Field(alias="policyId")


class NGFirewallZoneListEntry(BaseModel):
    src_zone_list_id: str = Field(validation_alias="srcZoneListId", serialization_alias="srcZoneListId")
    dst_zone_list_id: str = Field(validation_alias="dstZoneListId", serialization_alias="dstZoneListId")
    model_config = ConfigDict(populate_by_name=True)


class AssemblyItem(BaseModel):
    definition_id: str = Field(validation_alias="definitionId", serialization_alias="definitionId")
    type: str
    entries: Optional[Sequence[Any]] = None
    model_config = ConfigDict(populate_by_name=True)


class ZoneBasedFWAssemblyItem(AssemblyItem):
    type: Literal["zoneBasedFW"] = "zoneBasedFW"


class NGFirewallAssemblyItem(AssemblyItem):
    type: Literal["zoneBasedFW"] = "zoneBasedFW"
    entries: List[NGFirewallZoneListEntry] = []

    def add_zone_pair(self, src_zone_id: str, dst_zone_id: str):
        self.entries.append(NGFirewallZoneListEntry(src_zone_list_id=src_zone_id, dst_zone_list_id=dst_zone_id))


class DNSSecurityAssemblyItem(AssemblyItem):
    type: Literal["DNSSecurity"] = "DNSSecurity"


class IntrusionPreventionAssemblyItem(AssemblyItem):
    type: Literal["intrusionPrevention"] = "intrusionPrevention"


class URLFilteringAssemblyItem(AssemblyItem):
    type: Literal["urlFiltering"] = "urlFiltering"


class AdvancedMalwareProtectionAssemblyItem(AssemblyItem):
    type: Literal["advancedMalwareProtection"] = "advancedMalwareProtection"


class SSLDecryptionAssemblyItem(AssemblyItem):
    type: Literal["sslDecryption"] = "sslDecryption"


class PolicyDefinition(BaseModel):
    assembly: Sequence[AssemblyItem]


class PolicyCreationPayload(BaseModel):
    policy_name: str = Field(
        alias="policyName",
        pattern="^[a-zA-Z0-9_-]{1,127}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 127 characters",
    )
    policy_description: str = Field("Default description", alias="policyDescription")
    policy_type: str = Field(alias="policyType")
    policy_definition: PolicyDefinition = Field(alias="policyDefinition")
    is_policy_activated: bool = Field(default=False, alias="isPolicyActivated")
    model_config = ConfigDict(populate_by_name=True)


class PolicyEditPayload(PolicyCreationPayload, PolicyId):
    pass


class PolicyInfo(PolicyEditPayload):
    created_by: str = Field(alias="createdBy")
    created_on: datetime.datetime = Field(alias="createdOn")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    last_updated_on: datetime.datetime = Field(alias="lastUpdatedOn")
    policy_version: Optional[str] = Field(None, alias="policyVersion")


class PolicyPreview(BaseModel):
    preview: str
