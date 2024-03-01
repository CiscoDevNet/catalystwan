from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.utils.timezone import Timezone

ConsoleBaudRate = Literal["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
DefaultConsoleBaudRate = Literal["9600"]
Epfr = Literal["disabled", "aggressive", "moderate", "conservative"]
DefaultEpfr = Literal["disabled"]
SiteType = Literal["type-1", "type-2", "type-3", "cloud", "branch", "br", "spoke"]
DefaultTimezone = Literal["UTC"]


class Clock(BaseModel):
    timezone: Union[Variable, Global[Timezone], Default[DefaultTimezone]] = Field(
        default=as_default("UTC", DefaultTimezone), description="Set the timezone"
    )


class MobileNumberItem(BaseModel):
    number: Union[Global[str], Variable] = Field(..., description="Mobile number, ex: 1231234414")


class Sms(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    enable: Union[Global[bool], Default[bool]] = Field(
        default=as_default(False), description="Enable device’s geo fencing SMS"
    )
    mobile_number: Optional[List[MobileNumberItem]] = Field(
        None,
        serialization_alias="MobileNumber",
        validation_alias="MobileNumber",
        description="Set device’s geo fencing SMS phone number",
    )


class GeoFencing(BaseModel):
    enable: Union[Global[bool], Default[bool]] = Field(default=as_default(False), description="Enable Geo fencing")
    range: Union[Global[int], Variable, Default[int]] = Field(
        default=as_default(100), description="Set the device’s geo fencing range"
    )
    sms: Sms = Field(default_factory=Sms, description="Set device’s geo fencing SMS")  # type: ignore


class GpsVariable(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    longitude: Union[Variable, Global[float], Default[None]] = Field(
        default=Default[None](value=None), description="Set the device physical longitude"
    )
    latitude: Union[Variable, Global[float], Default[None]] = Field(
        default=Default[None](value=None), description="Set the device physical latitude"
    )
    geo_fencing: GeoFencing = Field(
        default_factory=GeoFencing,
        serialization_alias="geoFencing",
        validation_alias="geoFencing",
    )


class OnDemand(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    on_demand_enable: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="onDemandEnable",
        validation_alias="onDemandEnable",
        description="Enable or disable On-demand Tunnel",
    )
    on_demand_idle_timeout: Union[
        Variable,
        Global[int],
        Default[int],
    ] = Field(
        default=as_default(10),
        serialization_alias="onDemandIdleTimeout",
        validation_alias="onDemandIdleTimeout",
        description="Set the idle timeout for on-demand tunnels",
    )


class AffinityPerVrfItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    affinity_group_number: Union[
        Variable,
        Global[int],
        Default[None],
    ] = Field(
        default=Default[None](value=None),
        serialization_alias="affinityGroupNumber",
        validation_alias="affinityGroupNumber",
        description="Affinity Group Number",
    )
    vrf_range: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="vrfRange",
        validation_alias="vrfRange",
        description="Range of VRFs",
    )


class BasicParcel(_ParcelBase):
    type_: Literal["basic"] = Field(default="basic", exclude=True)

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    clock: Clock = Field(default_factory=Clock, validation_alias=AliasPath("data", "clock"))
    description: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "description"),
        description="Set a text description of the device",
    )
    location: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "location"),
        description="Set the location of the device",
    )
    gps_location: GpsVariable = Field(
        default_factory=GpsVariable,
        validation_alias=AliasPath("data", "gpsLocation"),
    )
    device_groups: Union[Variable, Global[List[str]], Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "deviceGroups"),
        description="Device groups",
    )
    controller_group_list: Optional[
        Union[
            Variable,
            Global[List[int]],
            Default[None],
        ]
    ] = Field(
        None,
        validation_alias=AliasPath("data", "controllerGroupList"),
        description="Configure a list of comma-separated controller groups",
    )
    overlay_id: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(1),
        validation_alias=AliasPath("data", "overlayId"),
        description="Set the Overlay ID",
    )
    port_offset: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(0),
        validation_alias=AliasPath("data", "portOffset"),
        description="Set the TLOC port offset when multiple devices are behind a NAT",
    )
    port_hop: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        validation_alias=AliasPath("data", "portHop"),
        description="Enable port hopping",
    )
    control_session_pps: Optional[Union[Variable, Global[int], Default[int]]] = Field(
        None,
        validation_alias=AliasPath("data", "controlSessionPps"),
        description="Set the policer rate for control sessions",
    )
    track_transport: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        None,
        validation_alias=AliasPath("data", "trackTransport"),
        description="Configure tracking of transport",
    )
    track_interface_tag: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        None,
        validation_alias=AliasPath("data", "trackInterfaceTag"),
        description="OMP Tag attached to routes based on interface tracking",
    )
    console_baud_rate: Union[Variable, Global[ConsoleBaudRate], Default[DefaultConsoleBaudRate]] = Field(
        default=as_default("9600", DefaultConsoleBaudRate),
        validation_alias=AliasPath("data", "consoleBaudRate"),
        description="Set the console baud rate",
    )
    max_omp_sessions: Union[Variable, Global[int], Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "maxOmpSessions"),
        description="Set the maximum number of OMP sessions <1..100> the device can have",
    )
    multi_tenant: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        None,
        validation_alias=AliasPath("data", "multiTenant"),
        description="Device is multi-tenant",
    )
    track_default_gateway: Optional[
        Union[
            Variable,
            Global[bool],
            Default[bool],
        ]
    ] = Field(
        None,
        validation_alias=AliasPath("data", "trackDefaultGateway"),
        description="Enable or disable default gateway tracking",
    )
    tracker_dia_stabilize_status: Optional[
        Union[
            Variable,
            Global[bool],
            Default[bool],
        ]
    ] = Field(
        None,
        validation_alias=AliasPath("data", "trackerDiaStabilizeStatus"),
        description="Enable or disable endpoint tracker diaStabilize status",
    )
    admin_tech_on_failure: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        validation_alias=AliasPath("data", "adminTechOnFailure"),
        description="Collect admin-tech before reboot due to daemon failure",
    )
    idle_timeout: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        None,
        validation_alias=AliasPath("data", "idleTimeout"),
        description="Idle CLI timeout in minutes",
    )
    on_demand: OnDemand = Field(
        default_factory=OnDemand,
        validation_alias=AliasPath("data", "onDemand"),
    )
    transport_gateway: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        None,
        validation_alias=AliasPath("data", "transportGateway"),
        description="Enable transport gateway",
    )
    epfr: Optional[Union[Global[Epfr], Default[DefaultEpfr], Variable]] = Field(
        None,
        validation_alias=AliasPath("data", "epfr"),
        description="Enable SLA Dampening and Enhanced App Routing.",
    )
    site_type: Optional[Union[Variable, Global[List[SiteType]], Default[None]]] = Field(
        None,
        validation_alias=AliasPath("data", "siteType"),
        description="Site Type",
    )
    affinity_group_number: Optional[
        Union[
            Variable,
            Global[int],
            Default[None],
        ]
    ] = Field(
        None,
        validation_alias=AliasPath("data", "affinityGroupNumber"),
        description="Affinity Group Number",
    )
    affinity_group_preference: Optional[
        Union[
            Variable,
            Global[List[int]],
            Default[None],
        ]
    ] = Field(
        None,
        validation_alias=AliasPath("data", "affinityGroupPreference"),
        description="Affinity Group Preference",
    )
    affinity_preference_auto: Optional[
        Union[
            Variable,
            Global[bool],
            Default[bool],
        ]
    ] = Field(
        None,
        validation_alias=AliasPath("data", "affinityPreferenceAuto"),
        description="Affinity Group Preference Auto",
    )
    affinity_per_vrf: Optional[List[AffinityPerVrfItem]] = Field(
        None,
        validation_alias=AliasPath("data", "affinityPerVrf"),
        description="Affinity Group Range for VRFs",
        max_length=4,
        min_length=0,
    )
