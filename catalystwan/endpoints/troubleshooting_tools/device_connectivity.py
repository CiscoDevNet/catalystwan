# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, post


class PingProbeType(str, Enum):
    ICMP = "icmp"
    TCP = "tcp"
    UDP = "udp"


class NPingRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    host: str
    vpn: str
    probe_type: PingProbeType = Field(default=PingProbeType.ICMP, serialization_alias="probeType")
    count: Optional[str] = None
    dest_port: Optional[str] = Field(default=None, serialization_alias="destPort")
    df: Optional[str] = None
    interface_ip: Optional[str] = Field(default=None, serialization_alias="interfaceIP")
    mtu: Optional[str] = None
    rapid: Optional[str] = None
    size: Optional[str] = None
    source: Optional[str] = None
    source_port: Optional[str] = Field(default=None, serialization_alias="sourcePort")
    tos: Optional[str] = None
    ttl: Optional[str] = None


class NPingResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    raw_output: List[str] = Field(validation_alias="rawOutput")
    packets_transmitted: int = Field(validation_alias="packetsTransmitted")
    packets_received: int = Field(validation_alias="packetsReceived")
    loss_percentage: float = Field(validation_alias="lossPercentage")
    min_round_trip: float = Field(validation_alias="minRoundTrip")
    max_round_trip: float = Field(validation_alias="maxRoundTrip")
    avg_round_trip: float = Field(validation_alias="avgRoundTrip")


class TroubleshootingToolsDeviceConnectivity(APIEndpoints):
    def copy_admin_tech_on_device(self):
        # POST /device/tools/admintech/copy
        ...

    def create_admin_tech(self):
        # POST /device/tools/admintech
        ...

    def delete_admin_tech_file(self):
        # DELETE /device/tools/admintech/{requestID}
        ...

    def delete_admin_tech_on_device(self):
        # DELETE /device/tools/admintech/delete
        ...

    def download_admin_tech_file(self):
        # GET /device/tools/admintech/download/{filename}
        ...

    def factory_reset(self):
        # POST /device/tools/factoryreset
        ...

    def get_control_connections(self):
        # GET /troubleshooting/control/{uuid}
        ...

    def get_device_configuration(self):
        # GET /troubleshooting/devicebringup
        ...

    def get_in_progress_count(self):
        # GET /device/tools/admintechs/inprogress
        ...

    def list_admin_techs(self):
        # GET /device/tools/admintechs
        ...

    def list_admin_techs_on_device(self):
        # POST /device/tools/admintechlist
        ...

    @post("/device/tools/nping/{device_ip}")
    def nping_device(self, device_ip: str, payload: NPingRequest) -> NPingResult:
        ...

    def ping_device(self):
        # POST /device/tools/ping/{deviceIP}
        ...

    def process_interface_reset(self):
        # POST /device/tools/reset/interface/{deviceIP}
        ...

    def process_port_hop_color(self):
        # POST /device/tools/porthopcolor/{deviceIP}
        ...

    def process_reset_user(self):
        # POST /device/tools/resetuser/{deviceIP}
        ...

    def service_path(self):
        # POST /device/tools/servicepath/{deviceIP}
        ...

    def traceroute_device(self):
        # POST /device/tools/traceroute/{deviceIP}
        ...

    def tunnel_path(self):
        # POST /device/tools/tunnelpath/{deviceIP}
        ...

    def upload_admin_tech(self):
        # POST /device/tools/admintechs/upload
        ...
