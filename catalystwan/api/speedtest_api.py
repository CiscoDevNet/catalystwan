# Copyright 2022 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
import math
from time import sleep
from typing import TYPE_CHECKING, cast
from urllib.error import HTTPError

from catalystwan.api.basic_api import DeviceStateAPI
from catalystwan.dataclasses import Device, Speedtest

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class SpeedtestAPI:
    """
    API methods to perform speedtest between 2 edge devices.

    Example:
        session = create_manager_session(...)
        devices = session.api.basic_api.devices
        speedtest = session.api.speedtest.speedtest(devices[0], devices[1])

        print(f"Upload speed from {speedtest.device_name} is {speedtest.up_speed} Mbps.)

        # example output: Upload speed from vm2 is 217.82 Mbps.

        speedtest is a Speedtest object containing source and destination device info and
            upload and download speed between them
    """

    def __init__(self, session: ManagerSession):
        self.session = session

    def speedtest(
        self,
        source_device: Device,
        destination_device: Device,
        test_duration_seconds: int = 300,
    ) -> Speedtest:
        """
        Performs speedtest between 2 edge devices.

        Args:
            source_device (Device): device from which the speed will be measured
            destination_device (Device): device to which the speed will be measured
            test_duration_seconds (int): duration of the speed measuring in seconds, defaults to 300 (5 minutes)
        """

        source_color = DeviceStateAPI(self.session).get_colors(source_device.id)[0]
        destination_color = DeviceStateAPI(self.session).get_colors(destination_device.id)[0]

        self.speedtest_output = Speedtest(
            device_ip=source_device.local_system_ip,
            device_name=source_device.hostname,
            destination_ip=destination_device.local_system_ip,
            destination_name=destination_device.hostname,
            status="",
            up_speed=0.0,
            down_speed=0.0,
        )  # type: ignore

        if source_device.is_reachable and destination_device.is_reachable:
            with DeviceStateAPI(self.session).enable_data_stream():
                try:
                    self.__perform(
                        source_device,
                        destination_device,
                        source_color,
                        destination_color,
                        test_duration_seconds,
                    )
                except HTTPError as e:
                    self.speedtest_output.status = str(e)
        else:
            self.speedtest_output.status = (
                f"Source is {source_device.reachability.value} and "
                f"destination device is {destination_device.reachability.value}"
            )

        return self.speedtest_output

    def __perform(
        self,
        source_device: Device,
        destination_device: Device,
        source_color: str,
        destination_color: str,
        test_duration_seconds: int = 300,
    ) -> None:
        start_query = {
            "deviceUUID": f"{source_device.uuid}",
            "sourceIp": f"{source_device.local_system_ip}",
            "sourceColor": f"{source_color}",
            "destinationIp": f"{destination_device.local_system_ip}",
            "destinationColor": f"{destination_color}",
            "port": "80",
        }
        url_path = "/dataservice/stream/device/speed"
        setup_speedtest = self.session.post(url_path, json=start_query).json()

        speedtest_session = setup_speedtest["sessionId"]

        self.session.get_json(f"/dataservice/stream/device/speed/start/{speedtest_session}")

        duration = math.ceil(test_duration_seconds / 5)
        for _ in range(duration):
            self.session.get_json(f"/dataservice/stream/device/speed/{speedtest_session}?logId=2")
            sleep(5)

        disable_speedtest = cast(
            dict,
            self.session.get_json(f"/dataservice/stream/device/speed/disable/{speedtest_session}"),
        )

        end_query = {
            "query": {
                "condition": "AND",
                "rules": [
                    {
                        "value": [f"{source_device.local_system_ip}"],
                        "field": "source_local_ip",
                        "type": "string",
                        "operator": "in",
                    },
                    {
                        "value": ["completed"],
                        "field": "status",
                        "type": "string",
                        "operator": "in",
                    },
                ],
            },
            "size": 10000,
        }
        url_path = "/dataservice/statistics/speedtest"
        post_speedtest = self.session.post(url_path, json=end_query).json()

        try:
            self.speedtest_output.status = disable_speedtest["status"]
            self.speedtest_output.up_speed = post_speedtest["data"][0]["up_speed"]
            self.speedtest_output.down_speed = post_speedtest["data"][0]["down_speed"]

            logger.info(
                f"Speedtest from {source_device.local_system_ip} " f"to {destination_device.local_system_ip} succeeded."
            )
        except IndexError:
            self.speedtest_output.status = "No speed received"
