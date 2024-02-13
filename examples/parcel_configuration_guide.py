import logging
import sys
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.models.common import TLOCColorEnum
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.application_list import (
    ApplicationListEntry,
    ApplicationListParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorEntry, ColorParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.data_prefix import (
    DataPrefixEntry,
    DataPrefixParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.payload_type import AnyPolicyObjectParcel

logger = logging.getLogger(__name__)

PROFILE_NAME = "Default_Policy_Object_Profile"


@dataclass
class CmdArguments:
    url: str
    port: int
    user: str
    password: str
    device_template: Optional[str] = None


def configure_groups_of_interest(profile: str, api: PolicyObjectFeatureProfileAPI):
    items: List[AnyPolicyObjectParcel] = []

    color_parcel = ColorParcel(
        parcel_name="ColorParcelExample",
        entries=[ColorEntry(color=as_global(TLOCColorEnum.LTE)), ColorEntry(color=as_global(TLOCColorEnum.GREEN))],
    )
    data_prefix_parcel = DataPrefixParcel(
        parcel_name="DataPrefixExample",
        entries=[DataPrefixEntry(ipv4_address=as_global(IPv4Address("10.0.0.0")), ipv4_prefix_length=as_global(16))],
    )
    application_list_parcel = ApplicationListParcel(
        parcel_name="AppListExample",
        entries=[
            ApplicationListEntry(app_list=as_global("3com-amp3")),
            ApplicationListEntry(app_list=as_global("sugarcrm")),
        ],
    )

    items.append(color_parcel)
    items.append(data_prefix_parcel)
    items.append(application_list_parcel)

    for item in items:
        print(item.model_dump_json(by_alias=True, indent=4))

    for item in items:
        api.create(profile, item)


def run_demo(args: CmdArguments):
    from catalystwan.session import create_manager_session

    with create_manager_session(
        url=args.url, port=args.port, username=args.user, password=args.password, logger=logger
    ) as session:
        api = PolicyObjectFeatureProfileAPI(session)
        configure_groups_of_interest(PROFILE_NAME, api)


def load_arguments() -> CmdArguments:
    url = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    return CmdArguments(url, int(port), user, password)


if __name__ == "__main__":
    arguments = load_arguments()
    run_demo(arguments)
