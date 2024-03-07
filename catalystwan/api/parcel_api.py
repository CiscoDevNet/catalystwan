# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.endpoints.configuration_feature_profile import ParcelId, SDRoutingConfigurationFeatureProfile
from catalystwan.models.feature_profile_parcel import FullConfig, FullConfigParcel


class ParcelAPI(Protocol):
    def create(self, name: str, description: str, data: dict) -> ParcelId:
        ...

    def edit(self, parcel_id: str, name: str, description: str, data: dict) -> None:
        ...

    def delete(self, parcel_id: str) -> None:
        ...


class SDRoutingFullConfigParcelAPI(ParcelAPI):
    def __init__(self, session: ManagerSession, fp_id: str):
        self.session = session
        self.fp_id = fp_id
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def create(self, name: str, description: str, data: dict) -> ParcelId:
        payload = FullConfigParcel(name=name, description=description, data=FullConfig(fullconfig=data["fullconfig"]))

        return self.endpoint.create_cli_full_config_parcel(self.fp_id, payload=payload)

    def edit(self, parcel_id: str, name: str, description: str, data: dict) -> None:
        payload = FullConfigParcel(name=name, description=description, data=FullConfig(fullconfig=data["fullconfig"]))

        self.endpoint.edit_cli_full_config_parcel(cli_fp_id=self.fp_id, parcel_id=parcel_id, payload=payload)

    def delete(self, parcel_id: str) -> None:
        self.endpoint.delete_cli_full_config_parcel(cli_fp_id=self.fp_id, parcel_id=parcel_id)
