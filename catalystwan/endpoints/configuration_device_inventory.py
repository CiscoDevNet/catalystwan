# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from pathlib import Path
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, CustomPayloadType, PreparedPayload, delete, get, post, versions
from catalystwan.typed_list import DataSequence
from catalystwan.utils.personality import Personality


class UnlockDeviceDetail(BaseModel):
    device_id: str = Field(validation_alias="deviceId", serialization_alias="deviceId")
    device_ip: str = Field(validation_alias="deviceIP", serialization_alias="deviceIP")


class DeviceUnlockPayload(BaseModel):
    device_type: str = Field(validation_alias="deviceType", serialization_alias="deviceType")
    devices: List[UnlockDeviceDetail]


class DeviceUnlockResponse(BaseModel):
    parentTaskId: str


Protocol = Literal["DTLS", "TLS"]


class DeviceCreationPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_ip: str = Field(alias="deviceIP")
    generate_csr: bool = Field(alias="generateCSR")
    password: str
    personality: Personality
    port: Optional[str] = Field(default=None)
    protocol: Protocol = Field(default="DTLS")
    username: str


class DeviceDeletionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    local_delete_from_db: Optional[bool] = Field(
        default=None, validation_alias="localDeleteFromDB", serialization_alias="localDeleteFromDB"
    )
    id: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)


DeviceCategory = Literal["controllers", "vedges"]


class DeviceDetailsResponse(BaseModel):
    # Field "model_sku" has conflict with protected namespace "model_"
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    device_type: Optional[str] = Field(default=None, validation_alias="deviceType", serialization_alias="deviceType")
    serial_number: Optional[str] = Field(
        default=None, validation_alias="serialNumber", serialization_alias="serialNumber"
    )
    uuid: Optional[str] = None
    management_system_ip: Optional[str] = Field(
        default=None, validation_alias="managementSystemIP", serialization_alias="managementSystemIP"
    )
    chasis_number: Optional[str] = Field(
        default=None, validation_alias="chasisNumber", serialization_alias="chasisNumber"
    )
    config_operation_mode: Optional[str] = Field(
        default=None, validation_alias="configOperationMode", serialization_alias="configOperationMode"
    )
    device_model: Optional[str] = Field(default=None, validation_alias="deviceModel", serialization_alias="deviceModel")
    device_state: Optional[str] = Field(default=None, validation_alias="deviceState", serialization_alias="deviceState")
    validity: Optional[str] = None
    platform_family: Optional[str] = Field(
        default=None, validation_alias="platformFamily", serialization_alias="platformFamily"
    )
    username: Optional[str] = None
    device_csr: Optional[str] = Field(default=None, validation_alias="deviceCSR", serialization_alias="deviceCSR")
    device_csr_common_name: Optional[str] = Field(
        default=None, validation_alias="deviceCSRCommonName", serialization_alias="deviceCSRCommonName"
    )
    root_cert_hash: Optional[str] = Field(
        default=None, validation_alias="rootCertHash", serialization_alias="rootCertHash"
    )
    csr: Optional[str] = Field(default=None, validation_alias="CSR", serialization_alias="CSR")
    csr_detail: Optional[str] = Field(default=None, validation_alias="CSRDetail", serialization_alias="CSRDetail")
    state: Optional[str] = None
    global_state: Optional[str] = Field(default=None, validation_alias="globalState", serialization_alias="globalState")
    valid: Optional[str] = None
    request_token_id: Optional[str] = Field(
        default=None, validation_alias="requestTokenID", serialization_alias="requestTokenID"
    )
    expiration_date: Optional[str] = Field(
        default=None, validation_alias="expirationDate", serialization_alias="expirationDate"
    )
    expiration_date_long: Optional[int] = Field(
        default=None, validation_alias="expirationDateLong", serialization_alias="expirationDateLong"
    )
    device_ip: Optional[str] = Field(default=None, validation_alias="deviceIP", serialization_alias="deviceIP")
    activity: Optional[List[str]] = None
    state_vedge_list: Optional[str] = Field(
        default=None, validation_alias="state_vedgeList", serialization_alias="state_vedgeList"
    )
    cert_install_status: Optional[str] = Field(
        default=None, validation_alias="certInstallStatus", serialization_alias="certInstallStatus"
    )
    org: Optional[str] = None
    personality: Optional[str] = None
    expiration_status: Optional[str] = Field(
        default=None, validation_alias="expirationStatus", serialization_alias="expirationStatus"
    )
    life_cycle_required: Optional[bool] = Field(
        default=None, validation_alias="lifeCycleRequired", serialization_alias="lifeCycleRequired"
    )
    hardware_cert_serial_number: Optional[str] = Field(
        default=None, validation_alias="hardwareCertSerialNumber", serialization_alias="hardwareCertSerialNumber"
    )
    subject_serial_number: Optional[str] = Field(
        default=None, validation_alias="subjectSerialNumber", serialization_alias="subjectSerialNumber"
    )
    resource_group: Optional[str] = Field(
        default=None, validation_alias="resourceGroup", serialization_alias="resourceGroup"
    )
    id: Optional[str] = None
    tags: Optional[List[str]] = None
    draft_mode: Optional[str] = Field(default=None, validation_alias="draftMode", serialization_alias="draftMode")
    solution: Optional[str] = None
    device_lock: Optional[str] = Field(default=None, validation_alias="device-lock", serialization_alias="device-lock")
    managed_by: Optional[str] = Field(default=None, validation_alias="managed-by", serialization_alias="managed-by")
    configured_site_id: Optional[str] = Field(
        default=None, validation_alias="configuredSiteId", serialization_alias="configuredSiteId"
    )
    ncs_device_name: Optional[str] = Field(
        default=None, validation_alias="ncsDeviceName", serialization_alias="ncsDeviceName"
    )
    config_status_message: Optional[str] = Field(
        default=None, validation_alias="configStatusMessage", serialization_alias="configStatusMessage"
    )
    template: Optional[str] = Field(default=None)
    template_id: Optional[str] = Field(default=None, validation_alias="templateId", serialization_alias="templateId")
    template_apply_log: Optional[List[str]] = Field(
        default=None, validation_alias="templateApplyLog", serialization_alias="templateApplyLog"
    )
    template_status: Optional[str] = Field(
        default=None, validation_alias="templateStatus", serialization_alias="templateStatus"
    )
    config_status_message_details: Optional[str] = Field(
        default=None, validation_alias="configStatusMessageDetails", serialization_alias="configStatusMessageDetails"
    )
    device_enterprise_certificate: Optional[str] = Field(
        default=None, validation_alias="deviceEnterpriseCertificate", serialization_alias="deviceEnterpriseCertificate"
    )
    service_personality: Optional[str] = Field(
        default=None, validation_alias="servicePersonality", serialization_alias="servicePersonality"
    )
    upload_source: Optional[str] = Field(
        default=None, validation_alias="uploadSource", serialization_alias="uploadSource"
    )
    time_remaining_for_expiration: Optional[int] = Field(
        default=None, validation_alias="timeRemainingForExpiration", serialization_alias="timeRemainingForExpiration"
    )
    domain_id: Optional[str] = Field(default=None, validation_alias="domain-id", serialization_alias="domain-id")
    local_system_ip: Optional[str] = Field(
        default=None, validation_alias="local-system-ip", serialization_alias="ocal-system-ip"
    )
    system_ip: Optional[str] = Field(default=None, validation_alias="system-ip", serialization_alias="system-ip")
    model_sku: Optional[str] = Field(default=None)
    site_id: Optional[str] = Field(default=None, validation_alias="site-id", serialization_alias="site-id")
    host_name: Optional[str] = Field(default=None, validation_alias="host-name", serialization_alias="host-name")
    sp_organization_name: Optional[str] = Field(
        default=None, validation_alias="sp-organization-name", serialization_alias="sp-organization-name"
    )
    version: Optional[str] = Field(default=None)
    vbond: Optional[str] = Field(default=None)
    vmanage_system_ip: Optional[str] = Field(
        default=None, validation_alias="vmanage-system-ip", serialization_alias="vmanage-system-ip"
    )
    vmanage_connection_state: Optional[str] = Field(
        default=None, validation_alias="vmanageConnectionState", serialization_alias="vmanageConnectionState"
    )
    last_updated: Optional[int] = Field(default=None, validation_alias="lastupdated", serialization_alias="lastupdated")
    reachability: Optional[str] = Field(default=None)
    uptime_date: Optional[int] = Field(default=None, validation_alias="uptime-date", serialization_alias="uptime-date")
    default_version: Optional[str] = Field(
        default=None, validation_alias="defaultVersion", serialization_alias="defaultVersion"
    )
    organization_name: Optional[str] = Field(
        default=None, validation_alias="organization-name", serialization_alias="organization-name"
    )
    available_versions: Optional[List[str]] = Field(
        default=None, validation_alias="availableVersions", serialization_alias="availableVersions"
    )
    site_name: Optional[str] = Field(default=None, validation_alias="site-name", serialization_alias="site-name")


class DeviceDetailsQueryParams(BaseModel):
    model: Optional[str] = None
    state: Optional[List[str]] = None
    uuid: Optional[List[str]] = None
    device_ip: Optional[List[str]] = Field(default=None, validation_alias="deviceIP", serialization_alias="deviceIP")
    validity: Optional[List[str]] = None
    family: Optional[str] = None


Validity = Literal["valid", "invalid"]


class SmartAccountSyncParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    password: str
    username: str
    validity_string: Validity = Field(default="valid")


class ProcessId(BaseModel):
    process_id: str = Field(validation_alias="processId", serialization_alias="processId")


class SerialFilePayload(CustomPayloadType):
    def __init__(self, image_path: str, validity: Validity = "valid"):
        self.image_path = image_path
        self.validity = validity
        self.data = open(self.image_path, "rb")
        self.fields = {"validity": self.validity, "upload": True}

    def prepared(self) -> PreparedPayload:
        return PreparedPayload(files={"file": (Path(self.data.name).name, self.data)}, data=self.fields)


ConfigType = Literal["cloudinit", "encodedstring"]


class GenerateBoostrapConfigurationQueryParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    configtype: Optional[ConfigType] = Field(default="cloudinit")
    incl_def_root_cert: Optional[bool] = Field(
        default=False, validation_alias="inclDefRootCert", serialization_alias="inclDefRootCert"
    )
    version: Optional[str] = Field(default="v1")


class BoostrapConfiguration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bootstrap_config: Optional[str] = Field(
        default=None, validation_alias="bootstrapConfig", serialization_alias="bootstrapConfig"
    )


class UploadSerialFileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vedge_list_upload_msg: Optional[str] = Field(
        default=None, validation_alias="vedgeListUploadMsg", serialization_alias="vedgeListUploadMsg"
    )
    vedge_list_upload_status: Optional[str] = Field(
        default=None, validation_alias="vedgeListUploadStatus", serialization_alias="vedgeListUploadStatus"
    )
    id: Optional[str] = None
    vedge_list_status_code: Optional[str] = Field(
        default=None, validation_alias="vedgeListStatusCode", serialization_alias="vedgeListStatusCode"
    )
    activity_list: Optional[Union[List, str]] = Field(
        default=None, validation_alias="activityList", serialization_alias="activityList"
    )


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
