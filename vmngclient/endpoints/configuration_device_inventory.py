# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, delete, get, post, versions
from vmngclient.typed_list import DataSequence
from vmngclient.utils.personality import Personality


class UnlockDeviceDetail(BaseModel):
    device_id: str = Field(alias="deviceId")
    device_ip: str = Field(alias="deviceIP")


class DeviceUnlockPayload(BaseModel):
    device_type: str = Field(alias="deviceType")
    devices: List[UnlockDeviceDetail]


class DeviceUnlockResponse(BaseModel):
    parentTaskId: str


class Protocol(str, Enum):
    DTLS = "DTLS"
    TLS = "TLS"


class DeviceCreationPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_ip: str = Field(alias="deviceIP")
    generate_csr: bool = Field(alias="generateCSR")
    password: str
    personality: Personality
    port: Optional[str] = Field(default=None)
    protocol: Protocol = Protocol.DTLS
    username: str


class DeviceDeletionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    local_delete_from_db: bool = Field(alias="localDeleteFromDB")
    id: str


class DeviceCategory(str, Enum):
    CONTROLLERS = "controllers"
    VEDGES = "vedges"


class DeviceDetailsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_type: str = Field(alias="deviceType")
    serial_number: str = Field(alias="serialNumber")
    uuid: str
    management_system_ip: str = Field(alias="managementSystemIP")
    chasis_number: str = Field(alias="chasisNumber")
    config_operation_mode: str = Field(alias="configOperationMode")
    device_model: str = Field(alias="deviceModel")
    device_state: str = Field(alias="deviceState")
    validity: str
    platform_family: str = Field(alias="platformFamily")
    username: str
    device_csr: Optional[str] = Field(default=None, alias="deviceCSR")
    device_csr_common_name: Optional[str] = Field(default=None, alias="deviceCSRCommonName")
    root_cert_hash: Optional[str] = Field(default=None, alias="rootCertHash")
    csr: Optional[str] = Field(default=None, alias="CSR")
    csr_detail: str = Field(default=None, alias="CSRDetail")
    state: Optional[str] = Field(default=None)
    global_state: Optional[str] = Field(default=None, alias="globalState")
    valid: Optional[str] = Field(default=None)
    request_token_id: Optional[str] = Field(default=None, alias="requestTokenID")
    expiration_date: str = Field(alias="expirationDate")
    expiration_date_long: Optional[int] = Field(default=None, alias="expirationDateLong")
    device_ip: str = Field(alias="deviceIP")
    activity: Optional[List[str]] = Field(default=None)
    state_vedge_list: Optional[str] = Field(default=None, alias="state_vedgeList")
    cert_install_status: Optional[str] = Field(default=None, alias="certInstallStatus")
    org: Optional[str] = Field(default=None)
    personality: str
    expiration_status: Optional[str] = Field(default=None, alias="expirationStatus")
    life_cycle_required: bool = Field(alias="lifeCycleRequired")
    hardware_cert_serial_number: str = Field(alias="hardwareCertSerialNumber")
    subject_serial_number: str = Field(alias="subjectSerialNumber")
    resource_group: str = Field(alias="resourceGroup")
    id: str
    tags: Optional[List[str]] = Field(default=None)
    draft_mode: Optional[str] = Field(default=None, alias="draftMode")
    solution: Optional[str] = Field(default=None)
    device_lock: str = Field(alias="device-lock")
    managed_by: str = Field(alias="managed-by")


class DeviceDetailsQueryParams(BaseModel):
    model: Optional[str] = None
    state: Optional[List[str]] = None
    uuid: Optional[List[str]] = None
    device_ip: Optional[List[str]] = Field(default=None, serialization_alias="deviceIP")
    validity: Optional[List[str]] = None
    family: Optional[str] = None


class ConfigurationDeviceInventory(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/system/device/{device_uuid}/unlock")
    def unlock(self, device_uuid: str, payload: DeviceUnlockPayload) -> DeviceUnlockResponse:
        ...

    @post("/system/device")
    def create_device(self, payload: DeviceCreationPayload) -> None:
        ...

    @delete("/system/device/{uuid}")
    def delete_device(self, uuid: str) -> DeviceDeletionResponse:
        ...

    @get("/system/device/{device_category}", "data")
    def get_device_details(
        self, device_category: DeviceCategory, params: DeviceDetailsQueryParams = DeviceDetailsQueryParams()
    ) -> DataSequence[DeviceDetailsResponse]:
        ...
