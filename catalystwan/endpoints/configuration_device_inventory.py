# mypy: disable-error-code="empty-body"
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, CustomPayloadType, PreparedPayload, delete, get, post, versions
from catalystwan.typed_list import DataSequence
from catalystwan.utils.personality import Personality


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
    # Field "model_sku" has conflict with protected namespace "model_"
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    device_type: Optional[str] = Field(default=None, alias="deviceType")
    serial_number: Optional[str] = Field(default=None, alias="serialNumber")
    uuid: Optional[str] = None
    management_system_ip: Optional[str] = Field(default=None, alias="managementSystemIP")
    chasis_number: Optional[str] = Field(default=None, alias="chasisNumber")
    config_operation_mode: Optional[str] = Field(default=None, alias="configOperationMode")
    device_model: Optional[str] = Field(default=None, alias="deviceModel")
    device_state: Optional[str] = Field(default=None, alias="deviceState")
    validity: Optional[str] = None
    platform_family: Optional[str] = Field(default=None, alias="platformFamily")
    username: Optional[str] = None
    device_csr: Optional[str] = Field(default=None, alias="deviceCSR")
    device_csr_common_name: Optional[str] = Field(default=None, alias="deviceCSRCommonName")
    root_cert_hash: Optional[str] = Field(default=None, alias="rootCertHash")
    csr: Optional[str] = Field(default=None, alias="CSR")
    csr_detail: Optional[str] = Field(default=None, alias="CSRDetail")
    state: Optional[str] = None
    global_state: Optional[str] = Field(default=None, alias="globalState")
    valid: Optional[str] = None
    request_token_id: Optional[str] = Field(default=None, alias="requestTokenID")
    expiration_date: Optional[str] = Field(default=None, alias="expirationDate")
    expiration_date_long: Optional[int] = Field(default=None, alias="expirationDateLong")
    device_ip: Optional[str] = Field(default=None, alias="deviceIP")
    activity: Optional[List[str]] = None
    state_vedge_list: Optional[str] = Field(default=None, alias="state_vedgeList")
    cert_install_status: Optional[str] = Field(default=None, alias="certInstallStatus")
    org: Optional[str] = None
    personality: Optional[str] = None
    expiration_status: Optional[str] = Field(default=None, alias="expirationStatus")
    life_cycle_required: Optional[bool] = Field(default=None, alias="lifeCycleRequired")
    hardware_cert_serial_number: Optional[str] = Field(default=None, alias="hardwareCertSerialNumber")
    subject_serial_number: Optional[str] = Field(default=None, alias="subjectSerialNumber")
    resource_group: Optional[str] = Field(default=None, alias="resourceGroup")
    id: Optional[str] = None
    tags: Optional[List[str]] = None
    draft_mode: Optional[str] = Field(default=None, alias="draftMode")
    solution: Optional[str] = None
    device_lock: Optional[str] = Field(default=None, alias="device-lock")
    managed_by: Optional[str] = Field(default=None, alias="managed-by")
    configured_site_id: Optional[str] = Field(default=None, alias="configuredSiteId")
    ncs_device_name: Optional[str] = Field(default=None, alias="ncsDeviceName")
    config_status_message: Optional[str] = Field(default=None, alias="configStatusMessage")
    template_apply_log: Optional[List[str]] = Field(default=None, alias="templateApplyLog")
    template_status: Optional[str] = Field(default=None, alias="templateStatus")
    config_status_message_details: Optional[str] = Field(default=None, alias="configStatusMessageDetails")
    device_enterprise_certificate: Optional[str] = Field(default=None, alias="deviceEnterpriseCertificate")
    service_personality: Optional[str] = Field(default=None, alias="servicePersonality")
    upload_source: Optional[str] = Field(default=None, alias="uploadSource")
    time_remaining_for_expiration: Optional[int] = Field(default=None, alias="timeRemainingForExpiration")
    domain_id: Optional[str] = Field(default=None, alias="domain-id")
    local_system_ip: Optional[str] = Field(default=None, alias="local-system-ip")
    system_ip: Optional[str] = Field(default=None, alias="system-ip")
    model_sku: Optional[str] = Field(default=None)
    site_id: Optional[str] = Field(default=None, alias="site-id")
    host_name: Optional[str] = Field(default=None, alias="host-name")
    sp_organization_name: Optional[str] = Field(default=None, alias="sp-organization-name")
    version: Optional[str] = Field(default=None)
    vbond: Optional[str] = Field(default=None)
    vmanage_system_ip: Optional[str] = Field(default=None, alias="vmanage-system-ip")
    vmanage_connection_state: Optional[str] = Field(default=None, alias="vmanageConnectionState")
    last_updated: Optional[int] = Field(default=None, alias="lastupdated")
    reachability: Optional[str] = Field(default=None)
    uptime_date: Optional[int] = Field(default=None, alias="uptime-date")
    default_version: Optional[str] = Field(default=None, alias="defaultVersion")
    organization_name: Optional[str] = Field(default=None, alias="organization-name")
    available_versions: Optional[List[str]] = Field(default=None, alias="availableVersions")
    site_name: Optional[str] = Field(default=None, alias="site-name")


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
    def unlock(self, device_uuid: UUID, payload: DeviceUnlockPayload) -> DeviceUnlockResponse:
        ...

    @post("/system/device")
    def create_device(self, payload: DeviceCreationPayload) -> None:
        ...

    @delete("/system/device/{uuid}")
    def delete_device(self, uuid: UUID) -> DeviceDeletionResponse:
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
        self, uuid: UUID, params: GenerateBoostrapConfigurationQueryParams = GenerateBoostrapConfigurationQueryParams()
    ) -> BoostrapConfiguration:
        ...
