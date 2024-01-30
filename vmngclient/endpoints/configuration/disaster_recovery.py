# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpoints, get, post


class DisasterRecovery(APIEndpoints):
    @post("/disasterrecovery/activate")
    def activate(self) -> None:
        ...

    @post("/disasterrecovery/deregister")
    def delete(self) -> None:
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

    @get("/disasterrecovery/clusterInfo")
    def get_cluster_info(self) -> None:
        ...

    # def get_config_db_restore_status(self) -> None:
    #     # GET /disasterrecovery/dbrestorestatus
    #     ...

    @get("/disasterrecovery/details")
    def get_details(self) -> None:
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
    def get_reachability_info(self) -> None:
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
    def pause_dr(self) -> None:
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
    def register(self) -> None:
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
