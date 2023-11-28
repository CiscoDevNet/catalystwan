# mypy: disable-error-code="empty-body"

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, delete


class DeviceDeletionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    local_delete_from_db: bool = Field(alias="localDeleteFromDB")
    id: str


class CertificateManagementDevice(APIEndpoints):
    @delete("/certificate/{uuid}")
    def delete_configuration(self, uuid: str) -> DeviceDeletionResponse:
        ...
