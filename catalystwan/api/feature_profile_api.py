# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, Type, Union, overload
from uuid import UUID

from catalystwan.typed_list import DataSequence

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.api.parcel_api import SDRoutingFullConfigParcelAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.policy_object import PolicyObjectFeatureProfile
from catalystwan.endpoints.configuration_feature_profile import SDRoutingConfigurationFeatureProfile
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    Parcel,
    ParcelCreationResponse,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    POLICY_OBJECT_PAYLOAD_ENDPOINT_MAPPING,
    AnyPolicyObjectParcel,
    ApplicationListParcel,
    AppProbeParcel,
    ColorParcel,
    DataPrefixParcel,
    ExpandedCommunityParcel,
    FowardingClassParcel,
    FQDNDomainParcel,
    GeoLocationListParcel,
    IPSSignatureParcel,
    IPv6DataPrefixParcel,
    IPv6PrefixListParcel,
    LocalDomainParcel,
    PolicierParcel,
    PreferredColorGroupParcel,
    PrefixListParcel,
    ProtocolListParcel,
    SecurityApplicationListParcel,
    SecurityDataPrefixParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    StandardCommunityParcel,
    TlocParcel,
    URLAllowParcel,
    URLBlockParcel,
)


class SDRoutingFeatureProfilesAPI:
    def __init__(self, session: ManagerSession):
        self.cli = SDRoutingCLIFeatureProfileAPI(session=session)
        self.policy_object = PolicyObjectFeatureProfileAPI(session=session)


class FeatureProfileAPI(Protocol):
    def init_parcels(self, fp_id: str) -> None:
        """
        Initialized parcel(s) associated with this feature profile
        """
        ...

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates feature profile
        """
        ...

    def delete(self, fp_id: str) -> None:
        """
        Deletes feature profile
        """
        ...


class SDRoutingCLIFeatureProfileAPI(FeatureProfileAPI):
    """
    SD-Routing CLI feature-profile APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def init_parcels(self, fp_id: str) -> None:
        """
        Initialize CLI full-config parcel associated with this feature profile
        """
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


class PolicyObjectFeatureProfileAPI:
    """
    SDWAN Feature Profile Policy Object APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = PolicyObjectFeatureProfile(session)

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ApplicationListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AppProbeParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ColorParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FowardingClassParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PolicierParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PrefixListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ProtocolListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityPortParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[TlocParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLAllowParcel]) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLBlockParcel]) -> DataSequence[Parcel[Any]]:
        ...

    # get by id

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ApplicationListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AppProbeParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ColorParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[FowardingClassParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PolicierParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PrefixListParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ProtocolListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityPortParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[TlocParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLAllowParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLBlockParcel], parcel_id: UUID) -> DataSequence[Parcel[Any]]:
        ...

    def get(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyPolicyObjectParcel],
        parcel_id: Union[UUID, None] = None,
    ) -> DataSequence[Parcel[Any]]:
        """
        Get all Policy Objects for selected profile_id and selected type or get one Policy Object given parcel id
        """

        policy_object_list_type = POLICY_OBJECT_PAYLOAD_ENDPOINT_MAPPING[parcel_type]
        if not parcel_id:
            return self.endpoint.get_all(profile_id=profile_id, policy_object_list_type=policy_object_list_type)
        parcel = self.endpoint.get_by_id(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=parcel_id
        )
        return DataSequence(Parcel, [parcel])

    def create(self, profile_id: UUID, payload: AnyPolicyObjectParcel) -> ParcelCreationResponse:
        """
        Create Policy Object for selected profile_id based on payload type
        """

        policy_object_list_type = POLICY_OBJECT_PAYLOAD_ENDPOINT_MAPPING[type(payload)]
        return self.endpoint.create(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, payload=payload
        )

    def update(self, profile_id: UUID, payload: AnyPolicyObjectParcel, list_object_id: UUID):
        """
        Update Policy Object for selected profile_id based on payload type
        """

        policy_type = POLICY_OBJECT_PAYLOAD_ENDPOINT_MAPPING[type(payload)]
        return self.endpoint.update(
            profile_id=profile_id, policy_object_list_type=policy_type, list_object_id=list_object_id, payload=payload
        )

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ApplicationListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[AppProbeParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ColorParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[FowardingClassParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[PolicierParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[PrefixListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[ProtocolListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityPortParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[TlocParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[URLAllowParcel], list_object_id: UUID) -> None:
        ...

    @overload
    def delete(self, profile_id: UUID, parcel_type: Type[URLBlockParcel], list_object_id: UUID) -> None:
        ...

    def delete(self, profile_id: UUID, parcel_type: Type[AnyPolicyObjectParcel], list_object_id: UUID) -> None:
        """
        Delete Policy Object for selected profile_id based on payload type
        """

        policy_object_list_type = POLICY_OBJECT_PAYLOAD_ENDPOINT_MAPPING[parcel_type]
        return self.endpoint.delete(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=list_object_id
        )
