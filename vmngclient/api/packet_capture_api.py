""" Methods for setting up packet capture session,
   and download .pcap session file.

    Returns:
        status: Status
"""
import logging
import time
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Iterator

from vmngclient.api.basic_api import DeviceStateAPI
from vmngclient.dataclasses import Device, PacketSetup, Status
from vmngclient.session import Session
from vmngclient.utils.creation_tools import create_dataclass, get_logger_name

logger = logging.getLogger(get_logger_name(__name__))


class DownloadStatus(Enum):
    COMPLETED = "COMPLETED"
    IMPOSSIBLE = "IMPOSSIBLE"
    FILESIZE = None


class PacketCaptureAPI:
    def __init__(self, session: Session, vpn: str = "0", interface: str = "ge0/1", status=None) -> None:
        self.session = session
        self.vpn = vpn
        self.interface = interface
        self.status = status

    def get_packets(self, device: Device, duration_time=20) -> Status:
        """Initate packet capture process.

        Args:
            device (Device): Device class object
            duration_time (int, optional): Duration od packet capturing . Defaults to 20.

        Returns:
            Status
        """
        with DeviceStateAPI(self.session).enable_data_stream():
            try:
                with self.channel(device):
                    with self.start_stop():
                        time.sleep(duration_time)
            except PermissionError as err:
                failed_status_dict = {
                    "fileDownloadStatus": DownloadStatus.IMPOSSIBLE.value,
                    "fileSize": DownloadStatus.FILESIZE.value,
                }
                self.status = create_dataclass(Status, failed_status_dict)
                logger.error(str(err))
            return self.status

    @contextmanager
    def channel(self, device: Device) -> Iterator:
        """Creates packet capture session.

        Args:
            device (Device): Device class object

        Raises:
            PermissionError: if already another packet capture session is active

        Yields:
            Iterator: packet_channel which contains session ID
        """
        query = {
            "deviceUUID": device.uuid,
            "vpn": self.vpn,
            "interface": self.interface,
            "type": "control",
        }

        try:
            url_path = r"/dataservice/stream/device/capture"
            packet_setup = dict(self.session.post_json(url_path, query))
            self.packet_channel = create_dataclass(PacketSetup, packet_setup)
            if self.packet_channel.is_new_session is True:
                yield self.packet_channel
            else:
                self.status = None
                raise PermissionError("Can't start new session, another is already open")
        finally:
            for _ in range(3):
                time.sleep(10)
                self.status = self.get_status(self.packet_channel)
                if self.status.file_download_status == DownloadStatus.COMPLETED.value:
                    self.download_capture_session(self.packet_channel, device)
                    url_path = f"/dataservice/stream/device/capture/disable/{self.packet_channel.session_id}"
                    self.session.get_json(url_path)
                    break

    @contextmanager
    def start_stop(self) -> Iterator:
        """Start and stops packet capturing.

        Yields:
            Iterator: None
        """
        try:
            url_path = f"/dataservice/stream/device/capture/start/{self.packet_channel.session_id}"
            self.session.get_json(url_path)
            yield None

        finally:
            url_path = f"/dataservice/stream/device/capture/stop/{self.packet_channel.session_id}"
            self.session.get_json(url_path)

    def get_interface_name(self, device: Device) -> str:

        url_path = f"/dataservice/device/interface/synced?deviceId={device.local_system_ip}"
        ifname = dict(self.session.get_json(url_path))
        if_name = str(ifname["data"][0]["ifname"])
        return if_name

    def download_capture_session(self, packet: PacketSetup, device: Device, file_path: str = None) -> bool:
        url_path = f"/dataservice/stream/device/capture/download/{packet.session_id}"
        full_url = self.session.get_full_url(url_path)
        download_packet = self.session.session_request("GET", full_url)
        if file_path is None:
            file_path = f"{Path(__file__).parents[0]}/{device.uuid}.pcap"

        with open(file_path, "wb") as file:
            with download_packet as raw:
                file.write(raw.read())
        return True

    def get_status(self, packet_channel: PacketSetup) -> Status:
        url_path = f"/dataservice/stream/device/capture/status/{packet_channel.session_id}"
        self.status = dict(self.session.get_json(url_path))
        self.status = create_dataclass(Status, self.status)
        return self.status
