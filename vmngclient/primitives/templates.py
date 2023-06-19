from typing import Dict

from pydantic import BaseModel, Field

from vmngclient.primitives import APIPrimitiveBase, view
from vmngclient.utils.session_type import ProviderView


class FeatureToCLIPayload(BaseModel):
    device_specific_variables: Dict[str, str] = Field(alias="device")
    is_edited: bool = Field(alias="isEdited")
    is_master_edited: bool = Field(alias="isMasterEdited")
    is_RFS_required: bool = Field(alias="isRFSRequired")
    template_id: str = Field(alias="templateId")


class TemplatesPrimitives(APIPrimitiveBase):
    @view({ProviderView})
    def get_device_configuration_preview(self, payload: FeatureToCLIPayload) -> str:
        response = self._post("/template/device/config/config/", payload=payload).text
        return response
