import logging
import math
from time import sleep
from typing import cast
from urllib.error import HTTPError

from vmngclient.api.basic_api import DeviceStateApi
from vmngclient.dataclasses import DeviceInfo, Speedtest
from vmngclient.session.session_base import Session
from vmngclient.utils.creation_tools import get_logger_name

logger = logging.getLogger(get_logger_name(__name__))


class SpeedtestApi:
    def __init__(self, session: Session):
        self.session = session

    def speedtest(
        self, source_device: DeviceInfo, destination_device: DeviceInfo, test_duration_seconds: int = 300
    ) -> Speedtest:

        source_color = DeviceStateApi(self.session).get_colors(source_device.id)[0]
        destination_color = DeviceStateApi(self.session).get_colors(destination_device.id)[0]

        self.speedtest_output = Speedtest(
            device_ip=source_device.local_system_ip,
            device_name=source_device.hostname,
            destination_ip=destination_device.local_system_ip,
            destination_name=destination_device.hostname,
            status="",
            up_speed=0,
            down_speed=0,
        )

        if source_device.is_reachable and destination_device.is_reachable:
            with DeviceStateApi(self.session).enable_data_stream():
                try:
                    self.perform(
                        source_device, destination_device, source_color, destination_color, test_duration_seconds
                    )
                except HTTPError as e:
                    self.speedtest_output.status = str(e)
        else:
            self.speedtest_output.status = f"Source is {source_device.reachability.value} and "
            f"destination device is {destination_device.reachability.value}"

        return self.speedtest_output

    def perform(
        self,
        source_device: DeviceInfo,
        destination_device: DeviceInfo,
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
        setup_speedtest = cast(dict, self.session.post_json(url_path, start_query))

        speedtest_session = setup_speedtest["sessionId"]

        self.session.get_json(f"/dataservice/stream/device/speed/start/{speedtest_session}")

        duration = math.ceil(test_duration_seconds / 5)
        for _ in range(duration):
            self.session.get_json(f"/dataservice/stream/device/speed/{speedtest_session}?logId=2")
            sleep(5)

        disable_speedtest = cast(
            dict, self.session.get_json(f"/dataservice/stream/device/speed/disable/{speedtest_session}")
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
                    {"value": ["completed"], "field": "status", "type": "string", "operator": "in"},
                ],
            },
            "size": 10000,
        }
        url_path = "/dataservice/statistics/speedtest"
        post_speedtest = cast(dict, self.session.post_json(url_path, end_query))

        try:
            self.speedtest_output.status = disable_speedtest["status"]
            self.speedtest_output.up_speed = post_speedtest["data"][0]["up_speed"]
            self.speedtest_output.down_speed = post_speedtest["data"][0]["down_speed"]

            logger.info(
                f"Speedtest from {source_device.local_system_ip} " f"to {destination_device.local_system_ip} succeeded."
            )
        except IndexError:
            self.speedtest_output.status = "No speed received"
