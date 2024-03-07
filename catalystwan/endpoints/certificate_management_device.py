# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, delete, post
from catalystwan.typed_list import DataSequence


class DeviceDeletionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    local_delete_from_db: Optional[bool] = Field(default=None, alias="localDeleteFromDB")
    id: Optional[UUID] = Field(default=None)


class TargetDevice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_ip: str = Field(alias="deviceIP")


class DeviceCsrGenerationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    globalState: Optional[str] = Field(default=None, alias="globalState")
    discoveredDeviceVpns: Optional[List[str]] = Field(default=None, alias="discoveredDeviceVpns")
    deviceConfigurationRfs: Optional[str] = Field(default=None, alias="deviceConfigurationRfs")
    configStatusMessageDetails: Optional[str] = Field(default=None, alias="configStatusMessageDetails")
    isPrestagingSupported: Optional[bool] = Field(default=None, alias="isPrestagingSupported")
    expirationStatus: Optional[str] = Field(default=None, alias="expirationStatus")
    uuid: Optional[UUID] = Field(default=None, alias="uuid")
    certificateDetail: Optional[str] = Field(default=None, alias="certificateDetail")
    createdAt: Optional[str] = Field(default=None, alias="createdAt")
    password: Optional[str] = Field(default=None, alias="password")
    solution: Optional[str] = Field(default=None, alias="solution")
    configOperationMode: Optional[str] = Field(default=None, alias="configOperationMode")
    state: Optional[str] = Field(default=None, alias="state")
    deviceType: Optional[str] = Field(default=None, alias="deviceType")
    serialNumber: Optional[str] = Field(default=None, alias="serialNumber")
    rootCertHash: Optional[str] = Field(default=None, alias="rootCertHash")
    deviceCSRCommonName: Optional[str] = Field(default=None, alias="deviceCSRCommonName")
    deviceConfiguration: Optional[str] = Field(default=None, alias="deviceConfiguration")
    CSRDetail: Optional[str] = Field(default=None, alias="CSRDetail")
    managementSystemIP: Optional[str] = Field(default=None, alias="managementSystemIP")
    deviceCSRGenTime: Optional[int] = Field(default=None, alias="deviceCSRGenTime")
    volatileUUID: Optional[UUID] = Field(default=None, alias="volatileUUID")
    deviceLifeCycleNeeded: Optional[bool] = Field(default=None, alias="deviceLifeCycleNeeded")
    deviceState: Optional[str] = Field(default=None, alias="deviceState")
    expirationDateLong: Optional[int] = Field(default=None, alias="expirationDateLong")
    timeRemainingForExpiration: Optional[int] = Field(default=None, alias="timeRemainingForExpiration")
    certInstallStatus: Optional[str] = Field(default=None, alias="certInstallStatus")
    activity: Optional[List[str]] = Field(default=None, alias="activity")
    deviceCSR: Optional[str] = Field(default=None, alias="deviceCSR")
    discoveredDeviceInterfaces: Optional[List[str]] = Field(default=None, alias="discoveredDeviceInterfaces")
    configuredSystemIP: Optional[str] = Field(default=None, alias="configuredSystemIP")
    platformFamily: Optional[str] = Field(default=None, alias="platformFamily")
    valid: Optional[str] = Field(default=None, alias="valid")
    templateStatus: Optional[str] = Field(default=None, alias="templateStatus")
    rid: Optional[int] = Field(default=None, alias="@rid")
    personality: Optional[str] = Field(default=None, alias="personality")
    hardwareVedge: Optional[bool] = Field(default=None, alias="hardwareVedge")
    chasisNumber: Optional[str] = Field(default=None, alias="chasisNumber")
    expirationDate: Optional[str] = Field(default=None, alias="expirationDate")
    deviceIP: Optional[str] = Field(default=None, alias="deviceIP")
    uploadSource: Optional[str] = Field(default=None, alias="uploadSource")
    deviceEnterpriseCertInstallTime: Union[str, int, None] = Field(
        default=None, alias="deviceEnterpriseCertInstallTime"
    )
    CSR: Optional[str] = Field(default=None, alias="CSR")
    deviceCSRGenTimeString: Optional[str] = Field(default=None, alias="deviceCSRGenTimeString")
    deviceEnterpriseCertificate: Optional[str] = Field(default=None, alias="deviceEnterpriseCertificate")
    ncsDeviceName: Optional[str] = Field(default=None, alias="ncsDeviceName")
    configStatusMessage: Optional[str] = Field(default=None, alias="configStatusMessage")
    requestTokenID: Optional[str] = Field(default=None, alias="requestTokenID")
    templateApplyLog: Optional[List[str]] = Field(default=None, alias="templateApplyLog")
    host_name: Optional[str] = Field(default=None, alias="host-name")
    createdBy: Optional[str] = Field(default=None, alias="createdBy")
    deviceModel: Optional[str] = Field(default=None, alias="deviceModel")
    validity: Optional[str] = Field(default=None, alias="validity")
    servicePersonality: Optional[str] = Field(default=None, alias="servicePersonality")
    configuredSiteId: Optional[str] = Field(default=None, alias="configuredSiteId")
    username: Optional[str] = Field(default=None, alias="username")
    local_system_ip: Optional[str] = Field(default=None, alias="local-system-ip")
    system_ip: Optional[str] = Field(default=None, alias="system-ip")
    site_id: Optional[str] = Field(default=None, alias="site-id")


class Validity(str, Enum):
    VALID = "valid"
    INVALID = "invalid"


class VedgeListValidityPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chasis_number: str = Field(alias="chasisNumber")
    serial_number: Optional[str] = Field(default=None, alias="serialNumber")
    validity: Validity = Field(default=Validity.INVALID)


class CertActionResponse(BaseModel):
    id: UUID


class CertificateManagementDevice(APIEndpoints):
    @delete("/certificate/{uuid}")
    def delete_configuration(self, uuid: str) -> DeviceDeletionResponse:
        ...

    @post("/certificate/generate/csr", "data")
    def generate_csr(self, payload: TargetDevice) -> DataSequence[DeviceCsrGenerationResponse]:
        ...

    @post("/certificate/save/vedge/list")
    def change_vedge_list_validity(self, payload: List[VedgeListValidityPayload]) -> CertActionResponse:
        ...

    @post("/certificate/vedge/list?action={action}")
    def send_to_controllers(self, action: str = "push") -> CertActionResponse:
        ...

    @post("/certificate/vsmart/list")
    def send_to_vbond(self) -> CertActionResponse:
        ...
