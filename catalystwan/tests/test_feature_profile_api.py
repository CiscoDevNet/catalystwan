import unittest
from unittest.mock import patch
from uuid import UUID

from parameterized import parameterized  # type: ignore

from catalystwan.api.feature_profile_api import SystemFeatureProfileAPI
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    AAAParcel,
    BannerParcel,
    BasicParcel,
    BFDParcel,
    GlobalParcel,
    LoggingParcel,
    MRFParcel,
    NTPParcel,
    OMPParcel,
    SecurityParcel,
    SNMPParcel,
)

endpoint_mapping = {
    AAAParcel: "aaa",
    BannerParcel: "banner",
    BasicParcel: "basic",
    BFDParcel: "bfd",
    GlobalParcel: "global",
    LoggingParcel: "logging",
    MRFParcel: "mrf",
    NTPParcel: "ntp",
    OMPParcel: "omp",
    SecurityParcel: "security",
    SNMPParcel: "snmp",
}


class TestSystemFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = UUID("054d1b82-9fa7-43c6-98fb-4355da0d77ff")
        self.parcel_uuid = UUID("7113505f-8cec-4420-8799-1a209357ba7e")

    @parameterized.expand(endpoint_mapping.items())
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.endpoints.configuration.feature_profile.sdwan.system.SystemFeatureProfile")
    def test_delete_method_with_valid_arguments(self, parcel, expected_path, mock_endpoint, mock_session):
        # Arrange
        api = SystemFeatureProfileAPI(mock_session)
        api.endpoint = mock_endpoint

        # Act
        api.delete_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        mock_endpoint.delete.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(endpoint_mapping.items())
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.endpoints.configuration.feature_profile.sdwan.system.SystemFeatureProfile")
    def test_get_method_with_valid_arguments(self, parcel, expected_path, mock_endpoint, mock_session):
        # Arrange
        api = SystemFeatureProfileAPI(mock_session)
        api.endpoint = mock_endpoint

        # Act
        api.get_parcels(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        mock_endpoint.get_by_id.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(endpoint_mapping.items())
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.endpoints.configuration.feature_profile.sdwan.system.SystemFeatureProfile")
    def test_get_all_method_with_valid_arguments(self, parcel, expected_path, mock_endpoint, mock_session):
        # Arrange
        api = SystemFeatureProfileAPI(mock_session)
        api.endpoint = mock_endpoint

        # Act
        api.get_parcels(self.profile_uuid, parcel)

        # Assert
        mock_endpoint.get_all.assert_called_once_with(self.profile_uuid, expected_path)

    @parameterized.expand(endpoint_mapping.items())
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.endpoints.configuration.feature_profile.sdwan.system.SystemFeatureProfile")
    def test_create_method_with_valid_arguments(self, parcel, expected_path, mock_endpoint, mock_session):
        # Arrange
        api = SystemFeatureProfileAPI(mock_session)
        api.endpoint = mock_endpoint

        # Act
        api.create_parcel(self.profile_uuid, parcel)

        # Assert
        mock_endpoint.create.assert_called_once_with(self.profile_uuid, expected_path, parcel)

    @parameterized.expand(endpoint_mapping.items())
    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.endpoints.configuration.feature_profile.sdwan.system.SystemFeatureProfile")
    def test_update_method_with_valid_arguments(self, parcel, expected_path, mock_endpoint, mock_session):
        # Arrange
        api = SystemFeatureProfileAPI(mock_session)
        api.endpoint = mock_endpoint

        # Act
        api.update(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        mock_endpoint.update.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid, parcel)
