# mypy: disable-error-code="empty-body"

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from vmngclient.endpoints import APIEndpoints, get


class TenancyModeEnum(str, Enum):
    st = "SingleTenant"
    mt = "MultiTenant"


class TenancyMode(BaseModel):
    mode: TenancyModeEnum
    deploymentmode: str
    domain: Optional[str] = None
    clusterid: Optional[str] = None


class ClusterManagement(APIEndpoints):
    def add_or_update_user_credentials(self):
        # POST /clusterManagement/userCreds
        ...

    def add_vmanage(self):
        # POST /clusterManagement/setup
        ...

    def check_if_cluster_locked(self):
        # GET /clusterManagement/clusterLocked
        ...

    def configure_vmanage(self):
        # POST /clusterManagement/configure
        ...

    def edit_vmanage(self):
        # PUT /clusterManagement/setup
        ...

    def get_cluster_workflow_version(self):
        # GET /clusterManagement/clusterworkflow/version
        ...

    def get_configured_ip_list(self):
        # GET /clusterManagement/iplist/{vmanageID}
        ...

    def get_connected_devices(self):
        # GET /clusterManagement/connectedDevices/{vmanageIP}
        ...

    def get_connected_devices_per_tenant(self):
        # GET /clusterManagement/{tenantId}/connectedDevices/{vmanageIP}
        ...

    @get("/clusterManagement/tenancy/mode", "data")
    def get_tenancy_mode(self) -> TenancyMode:
        ...

    def get_tenants_list(self):
        # GET /clusterManagement/tenantList
        ...

    def get_v_manage_details(self):
        # GET /clusterManagement/vManage/details/{vmanageIP}
        ...

    def health_details(self):
        # GET /clusterManagement/health/details
        ...

    def health_status_info(self):
        # GET /clusterManagement/health/status
        ...

    def health_summary(self):
        # GET /clusterManagement/health/summary
        ...

    def is_cluster_ready(self):
        # GET /clusterManagement/isready
        ...

    def list_vmanages(self):
        # GET /clusterManagement/list
        ...

    def node_properties(self):
        # GET /clusterManagement/nodeProperties
        ...

    def perform_replication_and_rebalance_of_kafka_partitions(self):
        # PUT /clusterManagement/replicateAndRebalance
        ...

    def remove_vmanage(self):
        # POST /clusterManagement/remove
        ...

    def set_tenancy_mode(self):
        # POST /clusterManagement/tenancy/mode
        ...
