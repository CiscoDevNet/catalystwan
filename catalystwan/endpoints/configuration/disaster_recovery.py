# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from ipaddress import IPv4Address
from typing import List, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, RootModel

from catalystwan.endpoints import APIEndpoints, get, post
from catalystwan.typed_list import DataSequence


class DisasterRecoveryTaskId(BaseModel):
    id: UUID


class RegisterDisasterRecoveryTaskId(DisasterRecoveryTaskId):
    ...


class DeregisterDisasterRecoveryTaskId(DisasterRecoveryTaskId):
    ...


class ActivateDisasterRecoveryTaskId(DisasterRecoveryTaskId):
    ...


class UnpauseDisasterRecoveryTaskId(DisasterRecoveryTaskId):
    ...


class ReplicationDetailsEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    last_replicated: str = Field(serialization_alias="lastReplicated", validation_alias="lastReplicated")
    export_duration: str = Field(serialization_alias="exportDuration", validation_alias="exportDuration")
    export_size: str = Field(serialization_alias="exportSize", validation_alias="exportSize")
    replication_status: str = Field(serialization_alias="replicationStatus", validation_alias="replicationStatus")
    export_id: str = Field(serialization_alias="exportID", validation_alias="exportID")


class DisasterRecoveryDetailsResponse(BaseModel):
    replication_details: List[ReplicationDetailsEntry]


class ValidateNodePayload(BaseModel):
    ip: IPv4Address
    username: str
    password: str


class ValidatedNodeEntry(BaseModel):
    ip: IPv4Address
    is_reachable: bool


class DisasterRecoveryPauseResponse(BaseModel):
    status: str


class DataCenter(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    nms_personality: str = Field(serialization_alias="nmsPersonality", validation_alias="nmsPersonality")
    dc_personality: str = Field(serialization_alias="dcPersonality", validation_alias="dcPersonality")
    management_ip: IPv4Address = Field(serialization_alias="mgmtIPAddress", validation_alias="mgmtIPAddress")
    username: str
    password: str


class DisasterRecoverySettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    delay_threshold: int = Field(serialization_alias="delayThreshold", validation_alias="delayThreshold")
    start_time: str = Field(serialization_alias="startTime", validation_alias="startTime")
    interval: int


class VbondPayload(BaseModel):
    name: str = Field(default="")
    ip: IPv4Address
    username: str
    password: str


class DisasterRecoveryRegisterPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data_centers: List[DataCenter] = Field(serialization_alias="dataCenters", validation_alias="dataCenters")
    disaster_recovery_settings: List[DisasterRecoverySettings] = Field(
        serialization_alias="disasterRecoverySettings", validation_alias="disasterRecoverySettings"
    )
    vbonds: List[VbondPayload]


class DisasterRecoveryStatusInformation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pause_replication: bool = Field(serialization_alias="pauseReplication", validation_alias="pauseReplication")
    pause_dr: bool = Field(serialization_alias="pauseDR", validation_alias="pauseDR")
    dr_enabled: bool = Field(serialization_alias="drenabled", validation_alias="drenabled")


class DisasterRecoveryStatusResponse(BaseModel):
    dr_status: Union[DisasterRecoveryStatusInformation, None] = Field(
        serialization_alias="drStatus", validation_alias="drStatus"
    )


class DisasterRecoveryScheduleResponse(BaseModel):
    schedule: DisasterRecoverySettings


class RemoteDataCentervManageVersionResponse(RootModel):
    root: list


class RemoteDataCenterDetails(BaseModel):
    name: str
    ip: IPv4Address
    uuid: UUID
    serialno: str
    state: str


class DisasterRecoveryDataCenterStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dc_personality: str = Field(serialization_alias="dcPersonality", validation_alias="dcPersonality")
    management_ip: IPv4Address = Field(serialization_alias="mgmtIPAddress", validation_alias="mgmtIPAddress")


class LastestLocalHistory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    last_switch: int = Field(serialization_alias="lastSwitch", validation_alias="lastSwitch")
    reason_for_switch: Union[str, None] = Field(
        serialization_alias="reasonForSwitch", validation_alias="reasonForSwitch"
    )
    updated_primary: Union[str, None] = Field(serialization_alias="updatedPrimary", validation_alias="updatedPrimary")


class ConfigurationDisasterRecovery(APIEndpoints):
    @post("/disasterrecovery/activate")
    def activate(self) -> ActivateDisasterRecoveryTaskId:
        ...

    @post("/disasterrecovery/deregister")
    def delete(self) -> DeregisterDisasterRecoveryTaskId:
        ...

    # def delete_dc(self) -> None:
    #     # POST /disasterrecovery/deleteRemoteDataCenter
    #     ...

    # def delete_local_dc(self) -> None:
    #     # POST /disasterrecovery/deleteLocalDataCenter
    #     ...

    # def disaster_recovery_pause_replication(self) -> None:
    #     # POST /disasterrecovery/pausereplication
    #     ...

    # def disaster_recovery_replication_request(self) -> None:
    #     # POST /disasterrecovery/requestimport
    #     ...

    # def disaster_recovery_un_pause_replication(self) -> None:
    #     # POST /disasterrecovery/unpausereplication
    #     ...

    # def download(self) -> None:
    #     # GET /disasterrecovery/download/backup/{token}/db_bkp.tar.gz
    #     ...

    # def download_replication_data(self) -> None:
    #     # GET /disasterrecovery/download/{token}/{fileName}
    #     ...

    # def get_usernames(self) -> None:
    #     # GET /disasterrecovery/usernames
    #     ...

    # @get("/disasterrecovery/clusterInfo")
    # def get_cluster_info(self) -> None:
    #     ...

    # def get_config_db_restore_status(self) -> None:
    #     # GET /disasterrecovery/dbrestorestatus
    #     ...

    @get("/disasterrecovery/details")
    def get_details(self) -> DisasterRecoveryDetailsResponse:
        ...

    @get("/disasterrecovery/schedule")
    def get_disaster_recovery_local_replication_schedule(self) -> DisasterRecoveryScheduleResponse:
        ...

    @get("/disasterrecovery/drstatus")
    def get_disaster_recovery_status(self) -> DataSequence[DisasterRecoveryDataCenterStatus]:
        ...

    # def get_history(self) -> None:
    #     # GET /disasterrecovery/history
    #     ...

    # def get_local_data_center_state(self) -> None:
    #     # GET /disasterrecovery/localdc
    #     ...

    @get("/disasterrecovery/localLatestHistory")
    def get_local_history(self) -> LastestLocalHistory:
        ...

    @post("/disasterrecovery/validateNodes")
    def get_reachability_info(self, payload: List[ValidateNodePayload]) -> DataSequence[ValidatedNodeEntry]:
        ...

    @get("/disasterrecovery/remotedc")
    def get_remote_data_center_details(self) -> DataSequence[RemoteDataCenterDetails]:
        ...

    @get("/disasterrecovery/remotedc/swversion")
    def get_remote_data_center_version(self) -> RemoteDataCentervManageVersionResponse:
        ...

    # def get_remote_dc_members_state(self) -> None:
    #     # GET /disasterrecovery/remoteDcState
    #     ...

    @get("/disasterrecovery/status")
    def get_dr_status(self) -> DisasterRecoveryStatusResponse:
        ...

    @post("/disasterrecovery/pause")
    def pause_dr(self) -> DisasterRecoveryPauseResponse:
        ...

    # def pause_local_arbitrator(self) -> None:
    #     # POST /disasterrecovery/pauseLocalArbitrator
    #     ...

    # def pause_local_dc_for_dr(self) -> None:
    #     # POST /disasterrecovery/pauseLocalDC
    #     ...

    # def pause_local_dc_replication(self) -> None:
    #     # POST /disasterrecovery/pauseLocalReplication
    #     ...

    @post("/disasterrecovery/register")
    def register(self, payload: DisasterRecoveryRegisterPayload) -> RegisterDisasterRecoveryTaskId:
        ...

    # def restart_data_center(self) -> None:
    #     # POST /disasterrecovery/restartDataCenter
    #     ...

    # def restore_config_db(self) -> None:
    #     # POST /disasterrecovery/dbrestore
    #     ...

    @post("/disasterrecovery/unpause")
    def unpause_dr(self) -> UnpauseDisasterRecoveryTaskId:
        ...

    # def unpause_local_arbitrator(self) -> None:
    #     # POST /disasterrecovery/unpauseLocalArbitrator
    #     ...

    # def unpause_local_dc_for_dr(self) -> None:
    #     # POST /disasterrecovery/unpauseLocalDC
    #     ...

    # def unpause_local_dc_replication(self) -> None:
    #     # POST /disasterrecovery/unpauseLocalReplication
    #     ...

    # def update(self) -> None:
    #     # POST /disasterrecovery/password
    #     ...

    # def update1(self) -> None:
    #     # PUT /disasterrecovery/register
    #     ...

    # def update_disaster_recovery_state(self) -> None:
    #     # POST /disasterrecovery/remotePassword
    #     ...

    # def update_disaster_recovery_state1(self) -> None:
    #     # POST /disasterrecovery/remotedc
    #     ...

    # def update_dr_state(self) -> None:
    #     # POST /disasterrecovery/updateDRConfigOnArbitrator
    #     ...

    # def update_replication(self) -> None:
    #     # POST /disasterrecovery/updateReplication
    #     ...
