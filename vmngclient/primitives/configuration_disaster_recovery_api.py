from typing import List

from pydantic import BaseModel, Field

from vmngclient.primitives import APIPrimitiveBase


class DataCenter(BaseModel):
    name: str = Field(alias="name")
    nms_personality: str = Field(alias="nmsPersonality")
    dc_personality: str = Field(alias="dcPersonality")
    mgmt_ip_address: str = Field(alias="mgmtIPAddress")
    username: str = Field(alias="username")
    password: str = Field(alias="password")


class DisasterRecoverySettings(BaseModel):
    start_time: str = Field(alias="startTime")
    interval: int = Field(alias="interval")


class Vbond(BaseModel):
    name: str = Field(alias="name")
    ip: str = Field(alias="ip")
    username: str = Field(alias="username")
    password: str = Field(alias="password")


class DatacenterRegistrationRequest(BaseModel):
    data_centers: List[DataCenter] = Field(alias="dataCenters")
    disaster_recovery_settings: DisasterRecoverySettings = Field(alias="disasterRecoverySettings")
    vbonds: List[Vbond] = Field(alias="vbonds")


class ConfigurationDisasterRecoveryApi(APIPrimitiveBase):
    def activate(self):
        # POST /disasterrecovery/activate
        ...

    def delete(self):
        # POST /disasterrecovery/deregister
        ...

    def delete_dc(self):
        # POST /disasterrecovery/deleteRemoteDataCenter
        ...

    def delete_local_dc(self):
        # POST /disasterrecovery/deleteLocalDataCenter
        ...

    def disaster_recovery_pause_replication(self):
        # POST /disasterrecovery/pausereplication
        ...

    def disaster_recovery_replication_request(self):
        # POST /disasterrecovery/requestimport
        ...

    def disaster_recovery_un_pause_replication(self):
        # POST /disasterrecovery/unpausereplication
        ...

    def download(self):
        # GET /disasterrecovery/download/backup/{token}/db_bkp.tar.gz
        ...

    def download_replication_data(self):
        # GET /disasterrecovery/download/{token}/{fileName}
        ...

    def get(self):
        # GET /disasterrecovery/usernames
        ...

    def get_cluster_info(self):
        # GET /disasterrecovery/clusterInfo
        ...

    def get_config_db_restore_status(self):
        # GET /disasterrecovery/dbrestorestatus
        ...

    def get_details(self):
        # GET /disasterrecovery/details
        ...

    def get_disaster_recovery_local_replication_schedule(self):
        # GET /disasterrecovery/schedule
        ...

    def get_disaster_recovery_status(self):
        # GET /disasterrecovery/drstatus
        ...

    def get_history(self):
        # GET /disasterrecovery/history
        ...

    def get_local_data_center_state(self):
        # GET /disasterrecovery/localdc
        ...

    def get_local_history(self):
        # GET /disasterrecovery/localLatestHistory
        ...

    def get_reachability_info(self):
        # POST /disasterrecovery/validateNodes
        ...

    def get_remote_data_center_state(self):
        # GET /disasterrecovery/remotedc
        ...

    def get_remote_data_center_version(self):
        # GET /disasterrecovery/remotedc/swversion
        ...

    def get_remote_dc_members_state(self):
        # GET /disasterrecovery/remoteDcState
        ...

    def getdr_status(self):
        # GET /disasterrecovery/status
        ...

    def pause_dr(self):
        # POST /disasterrecovery/pause
        ...

    def pause_local_arbitrator(self):
        # POST /disasterrecovery/pauseLocalArbitrator
        ...

    def pause_local_dc_for_dr(self):
        # POST /disasterrecovery/pauseLocalDC
        ...

    def pause_local_dc_replication(self):
        # POST /disasterrecovery/pauseLocalReplication
        ...

    def register(self, request: DatacenterRegistrationRequest):
        return self.post("/disasterrecovery/register", json=request.json)

    def restart_data_center(self):
        # POST /disasterrecovery/restartDataCenter
        ...

    def restore_config_db(self):
        # POST /disasterrecovery/dbrestore
        ...

    def unpause_dr(self):
        # POST /disasterrecovery/unpause
        ...

    def unpause_local_arbitrator(self):
        # POST /disasterrecovery/unpauseLocalArbitrator
        ...

    def unpause_local_dc_for_dr(self):
        # POST /disasterrecovery/unpauseLocalDC
        ...

    def unpause_local_dc_replication(self):
        # POST /disasterrecovery/unpauseLocalReplication
        ...

    def update(self):
        # POST /disasterrecovery/password
        ...

    def update1(self):
        # PUT /disasterrecovery/register
        ...

    def update_disaster_recovery_state(self):
        # POST /disasterrecovery/remotePassword
        ...

    def update_disaster_recovery_state1(self):
        # POST /disasterrecovery/remotedc
        ...

    def update_dr_state(self):
        # POST /disasterrecovery/updateDRConfigOnArbitrator
        ...

    def update_replication(self):
        # POST /disasterrecovery/updateReplication
        ...
