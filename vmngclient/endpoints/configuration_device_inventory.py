# mypy: disable-error-code="empty-body"
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, CustomPayloadType, PreparedPayload, delete, get, post, versions
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

    local_delete_from_db: Optional[bool] = Field(default=None, alias="localDeleteFromDB")
    id: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)


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
    platform_family: Optional[str] = Field(default=None, alias="platformFamily")
    username: Optional[str] = Field(default=None)
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
    device_ip: Optional[str] = Field(default=None, alias="deviceIP")
    activity: Optional[List[str]] = Field(default=None)
    state_vedge_list: Optional[str] = Field(default=None, alias="state_vedgeList")
    cert_install_status: Optional[str] = Field(default=None, alias="certInstallStatus")
    org: Optional[str] = Field(default=None)
    personality: str
    expiration_status: Optional[str] = Field(default=None, alias="expirationStatus")
    life_cycle_required: bool = Field(alias="lifeCycleRequired")
    hardware_cert_serial_number: str = Field(alias="hardwareCertSerialNumber")
    subject_serial_number: str = Field(alias="subjectSerialNumber")
    resource_group: Optional[str] = Field(default=None, alias="resourceGroup")
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


class Validity(str, Enum):
    VALID = "valid"
    INVALID = "invalid"


class SmartAccountSyncParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    password: str
    username: str
    validity_string: str = Validity.INVALID


class ProcessId(BaseModel):
    process_id: str = Field(alias="processId")


class SerialFilePayload(CustomPayloadType):
    def __init__(self, image_path: str, validity: Validity = Validity.INVALID):
        self.image_path = image_path
        self.validity = validity
        self.data = open(self.image_path, "rb")
        self.fields = {"validity": self.validity, "upload": True}

    def prepared(self) -> PreparedPayload:
        return PreparedPayload(files={"file": (Path(self.data.name).name, self.data)}, data=self.fields)


class ConfigType(str, Enum):
    CLOUDINIT = "cloudinit"
    ENCODEDSTRING = "encodedstring"


class GenerateBoostrapConfigurationQueryParams(BaseModel):
    configtype: Optional[ConfigType] = Field(default=ConfigType.CLOUDINIT)
    incl_def_root_cert: Optional[bool] = Field(default=False)
    version: Optional[str] = Field(default="v1")


class BoostrapConfiguration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bootstrap_config: Optional[str] = Field(default=None, alias="bootstrapConfig")


class UploadSerialFileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vedge_list_upload_msg: Optional[str] = Field(default=None, alias="vedgeListUploadMsg")
    vedge_list_upload_status: Optional[str] = Field(default=None, alias="vedgeListUploadStatus")
    id: Optional[str] = None
    vedge_list_status_code: Optional[str] = Field(default=None, alias="vedgeListStatusCode")
    activity_list: Optional[Union[List, str]] = Field(default=None, alias="activityList")


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

    # Covers:
    # url = "/dataservice/system/device/controllers"
    # url = "/dataservice/system/device/vedges"
    @get("/system/device/{device_category}", "data")
    def get_device_details(
        self, device_category: DeviceCategory, params: DeviceDetailsQueryParams = DeviceDetailsQueryParams()
    ) -> DataSequence[DeviceDetailsResponse]:
        ...

    @post("/system/device/smartaccount/sync")
    def sync_devices_from_smart_account(self, payload: SmartAccountSyncParams) -> ProcessId:
        ...

    @post("/system/device/fileupload")
    def upload_wan_edge_list(self, payload: SerialFilePayload) -> UploadSerialFileResponse:
        ...

    @get("/system/device/bootstrap/device/{uuid}")
    def generate_bootstrap_configuration(
        self, uuid: str, params: GenerateBoostrapConfigurationQueryParams = GenerateBoostrapConfigurationQueryParams()
    ) -> BoostrapConfiguration:
        ...
