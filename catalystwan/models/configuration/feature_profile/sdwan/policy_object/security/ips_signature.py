# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class IPSSignatureListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    generator_id: Global[str] = Field(
        serialization_alias="generatorId", validation_alias="generatorId", description="Range 0 to 4294967295"
    )
    signature_id: Global[str] = Field(
        serialization_alias="signatureId", validation_alias="signatureId", description="Range 0 to 4294967295"
    )

    @field_validator("generator_id")
    @classmethod
    def check_generator_id(cls, generator_id: Global):
        assert 0 <= int(generator_id.value) <= 4294967295
        return generator_id

    @field_validator("signature_id")
    @classmethod
    def check_signature_id(cls, signature_id: Global):
        assert 0 <= int(signature_id.value) <= 4294967295
        return signature_id


class IPSSignatureParcel(_ParcelBase):
    type_: Literal["security-ipssignature"] = Field(default="security-ipssignature", exclude=True)
    entries: List[IPSSignatureListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_signature(self, signature: str):
        generator_id, signature_id = signature.split(":")
        self.entries.append(
            IPSSignatureListEntry(
                generator_id=as_global(generator_id),
                signature_id=as_global(signature_id),
            )
        )
