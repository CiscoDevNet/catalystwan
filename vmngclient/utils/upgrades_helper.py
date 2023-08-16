from enum import Enum
from pathlib import PurePath

from attr import define  # type: ignore
from clint.textui.progress import Bar as ProgressBar  # type: ignore
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor  # type: ignore

from vmngclient.dataclasses import Device
from vmngclient.endpoints import CustomPayloadType, PreparedPayload
from vmngclient.exceptions import MultiplePersonalityError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.personality import Personality


class Family(Enum):
    VEDGE = "vedge"
    VMANAGE = "vmanage"


class VersionType(Enum):
    VMANAGE = "vmanage"


class DeviceType(Enum):
    CONTROLLER = "controller"
    VEDGE = "vedge"
    VMANAGE = "vmanage"


@define
class InstallSpecification:
    family: Family
    version_type: VersionType
    device_type: DeviceType


class InstallSpecHelper(Enum):
    """
    Container class for storage payload data for all personalities.
    It's created, because personality is not clearly connected to Family, VersionType
    or DeviceType
    """

    VMANAGE = InstallSpecification(Family.VMANAGE, VersionType.VMANAGE, DeviceType.VMANAGE)  # type: ignore
    VSMART = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.CONTROLLER)  # type: ignore
    VBOND = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.CONTROLLER)  # type: ignore
    VEDGE = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.VEDGE)  # type: ignore


def get_install_specification(device: Device):
    specification_container = {
        Personality.VMANAGE: InstallSpecHelper.VMANAGE.value,
        Personality.VBOND: InstallSpecHelper.VBOND.value,
        Personality.VSMART: InstallSpecHelper.VSMART.value,
        Personality.EDGE: InstallSpecHelper.VEDGE.value,
    }
    return specification_container[device.personality]


def validate_personality_homogeneity(devices: DataSequence[Device]):
    personalities = set([device.personality for device in devices])
    if not len(personalities) == 1:
        raise MultiplePersonalityError(
            f"devices has got more than 1 personality, devices personalities: {personalities}"
        )


class SoftwarePackageUpdatePayload(CustomPayloadType):
    def __init__(self, image_path: str):
        encoder = MultipartEncoder(
            fields={"file": (PurePath(image_path).name, open(image_path, "rb"), "application/x-gzip")}
        )
        callback = self._create_callback(encoder)
        monitor = MultipartEncoderMonitor(encoder, callback)
        self.payload = PreparedPayload(data=monitor, headers={"content-type": monitor.content_type})

    def _create_callback(self, encoder: MultipartEncoder):
        bar = ProgressBar(expected_size=encoder._calculate_length(), filled_char="=")

        def callback(monitor: MultipartEncoderMonitor):
            bar.show(monitor.bytes_read)

        return callback

    def prepared(self) -> PreparedPayload:
        return self.payload
