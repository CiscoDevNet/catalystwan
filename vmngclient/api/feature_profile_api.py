from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.api.parcel_api import SDRoutingFullConfigParcelAPI
from vmngclient.endpoints.configuration_feature_profile import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    SDRoutingConfigurationFeatureProfile,
)


class SDRoutingFeatureProfilesAPI:
    def __init__(self, session: vManageSession):
        self.cli = SDRoutingCLIFeatureProfileAPI(session=session)


class FeatureProfileAPI(ABC):
    def __init__(self, session: vManageSession):
        self.session = session

    @abstractmethod
    def init_parcels(self, fp_id: str) -> None:
        """
        Initialized parcel(s) associated with this feature profile
        """
        pass

    @abstractmethod
    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates feature profile
        """
        pass

    @abstractmethod
    def delete(self, fp_id: str) -> None:
        """
        Deletes feature profile
        """
        pass


class SDRoutingCLIFeatureProfileAPI(FeatureProfileAPI):
    """
    SD-Routing CLI feature-profile APIs
    """

    def __init__(self, session: vManageSession):
        super().__init__(session)
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def init_parcels(self, fp_id: str) -> None:
        self.full_config_parcel = SDRoutingFullConfigParcelAPI(session=self.session, fp_id=fp_id)

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates CLI feature profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)

        return self.endpoint.create_cli_feature_profile(payload=payload)

    def delete(self, fp_id: str) -> None:
        """
        Deletes CLI feature-profile
        """
        self.endpoint.delete_cli_feature_profile(cli_fp_id=fp_id)
