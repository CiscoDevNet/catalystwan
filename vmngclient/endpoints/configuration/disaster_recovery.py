# mypy: disable-error-code="empty-body"
from ipaddress import IPv4Address
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.endpoints import APIEndpoints, get, post
from vmngclient.typed_list import DataSequence


class DisasterRecoveryTaskId(BaseModel):
    id: UUID


class RegisterDisasterRecoveryTaskId(DisasterRecoveryTaskId):
    ...


class DeregisterDisasterRecoveryTaskId(DisasterRecoveryTaskId):
    ...


class ActivateDisasterRecoveryTaskId(DisasterRecoveryTaskId):
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

    # def get_disaster_recovery_local_replication_schedule(self) -> None:
    #     # GET /disasterrecovery/schedule
    #     ...

    # def get_disaster_recovery_status(self) -> None:
    #     # GET /disasterrecovery/drstatus
    #     ...

    # def get_history(self) -> None:
    #     # GET /disasterrecovery/history
    #     ...

    # def get_local_data_center_state(self) -> None:
    #     # GET /disasterrecovery/localdc
    #     ...

    # def get_local_history(self) -> None:
    #     # GET /disasterrecovery/localLatestHistory
    #     ...

    @post("/disasterrecovery/validateNodes")
    def get_reachability_info(self, payload: List[ValidateNodePayload]) -> DataSequence[ValidatedNodeEntry]:
        ...

    # def get_remote_data_center_state(self) -> None:
    #     # GET /disasterrecovery/remotedc
    #     ...

    # def get_remote_data_center_version(self) -> None:
    #     # GET /disasterrecovery/remotedc/swversion
    #     ...

    # def get_remote_dc_members_state(self) -> None:
    #     # GET /disasterrecovery/remoteDcState
    #     ...

    # def getdr_status(self) -> None:
    #     # GET /disasterrecovery/status
    #     ...

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

    # def unpause_dr(self) -> None:
    #     # POST /disasterrecovery/unpause
    #     ...

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
