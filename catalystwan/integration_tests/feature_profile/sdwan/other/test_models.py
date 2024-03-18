import os
import unittest
from typing import cast

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.other import ThousandEyesParcel, UcseParcel
from catalystwan.models.configuration.feature_profile.sdwan.other.ucse import AccessPort, Imc, LomType, SharedLom
from catalystwan.session import create_manager_session


class TestSystemOtherProfileModels(unittest.TestCase):
    def setUp(self) -> None:
        self.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )
        self.profile_id = self.session.api.sdwan_feature_profiles.other.create_profile("TestProfile", "Description").id

    def test_when_default_values_thousandeyes_parcel_expect_successful_post(self):
        # Arrange
        te_parcel = ThousandEyesParcel(
            parcel_name="ThousandEyesDefault",
            parcel_description="ThousandEyes Parcel",
        )
        # Act
        parcel_id = self.session.api.sdwan_feature_profiles.other.create_parcel(self.profile_id, te_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_ucse_parcel_expect_successful_post(self):
        # Arrange
        ucse_parcel = UcseParcel(
            parcel_name="UcseDefault",
            parcel_description="Ucse Parcel",
            bay=as_global(1),
            slot=as_global(2),
            imc=Imc(
                access_port=AccessPort(
                    shared_lom=SharedLom(
                        lom_type=Global[LomType](value="te2"),
                    )
                )
            ),
        )
        # Act
        parcel_id = self.session.api.sdwan_feature_profiles.other.create_parcel(self.profile_id, ucse_parcel).id
        # Assert
        assert parcel_id

    def tearDown(self) -> None:
        self.session.api.sdwan_feature_profiles.other.delete_profile(self.profile_id)
        self.session.close()
