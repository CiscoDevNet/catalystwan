# mypy: disable-error-code="empty-body"

from typing import Optional

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get, request


class CloudConnector(BaseModel):
    cloud_enabled: bool = Field(alias="cloudEnabled")
    client_id: Optional[str] = Field(default=None, alias="clientId")
    client_secret: Optional[str] = Field(default=None, alias="clientSecret")
    org_name: Optional[str] = Field(default=None, alias="orgName")
    affinity: Optional[str] = None
    telemetry_enabled: Optional[bool] = Field(default=None, alias="telemetryEnabled")


class SDAVCCloudConnector(APIEndpoints):
    def disable_cloud_connector(self):
        # PUT /sdavc/cloudconnector
        ...

    def enable_cloud_connector(self):
        # POST /sdavc/cloudconnector
        ...

    @request(get, "/sdavc/cloudconnector")
    def get_cloud_connector(self) -> CloudConnector:
        ...

    def get_cloud_connector_status(self):
        # GET /sdavc/cloudconnector/status
        ...
