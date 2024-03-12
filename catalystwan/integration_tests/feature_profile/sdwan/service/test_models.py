import os
import unittest
from ipaddress import IPv4Address
from typing import cast

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    AddressPool,
    LanVpnDhcpServerParcel,
    SubnetMask,
)
from catalystwan.session import create_manager_session


class TestServiceFeatureProfileModels(unittest.TestCase):
    def setUp(self) -> None:
        self.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )
        self.profile_id = self.session.api.sdwan_feature_profiles.service.create_profile(
            "TestProfile", "Description"
        ).id

    def test_when_default_values_dhcp_server_parcel_expect_successful_post(self):
        # Arrange
        url = f"dataservice/v1/feature-profile/sdwan/service/{self.profile_id}/dhcp-server"
        dhcp_server_parcel = LanVpnDhcpServerParcel(
            parcel_name="DhcpServerDefault",
            parcel_description="Dhcp Server Parcel",
            address_pool=AddressPool(
                network_address=Global[IPv4Address](value=IPv4Address("10.0.0.2")),
                subnet_mask=Global[SubnetMask](value="255.255.255.255"),
            ),
        )
        # Act
        response = self.session.post(
            url=url, data=dhcp_server_parcel.model_dump_json(by_alias=True, exclude_none=True)
        )  # This will be changed to the actual method
        # Assert
        assert response.status_code == 200

    def tearDown(self) -> None:
        self.session.api.sdwan_feature_profiles.service.delete_profile(self.profile_id)
        self.session.close()
