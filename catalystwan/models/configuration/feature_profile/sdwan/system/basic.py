from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

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
        default=as_default("UTC"), description="Set the timezone"
    )


class MobileNumberItem(BaseModel):
    number: Union[Global[str], Variable] = Field(..., description="Mobile number, ex: 1231234414")


class Sms(BaseModel):
    enable: Optional[Union[Global[bool], Default[Literal[False]]]] = Field(
        None, description="Global[bool] device’s geo fencing SMS"
    )
    mobile_number: Optional[List[MobileNumberItem]] = Field(
        None,
        serialization_alias="MobileNumber",
        validation_alias="MobileNumber",
        description="Set device’s geo fencing SMS phone number",
    )


class GeoFencing(BaseModel):
    enable: Optional[Union[Global[bool], Default[Literal[False]]]] = Field(None, description="Enable Geo fencing")
    range: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        None, description="Set the device’s geo fencing range"
    )
    sms: Optional[Sms] = None


class GpsVariable(BaseModel):
    longitude: Union[Variable, Global[float], Default[None]] = Field(
        default=as_default(None), description="Set the device physical longitude"
    )
    latitude: Union[Variable, Global[float], Default[None]] = Field(
        default=as_default(None), description="Set the device physical latitude"
    )
    geo_fencing: Optional[GeoFencing] = Field(
        None,
        serialization_alias="geoFencing",
        validation_alias="geoFencing",
    )


class OnDemand(BaseModel):
    on_demand_enable: Union[Variable, Global[bool], Default[Literal[False]]] = Field(
        default=False,
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
        serialization_alias="onDemandVariable",
        validation_alias="onDemandVariable",
        description="Set the idle timeout for on-demand tunnels",
    )


class AffinityPerVrfItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    affinity_group_number: Union[
        Variable,
        Global[int],
        Default[None],
    ] = Field(
        default=as_default(None),
        serialization_alias="affinityGroupNumber",
        validation_alias="affinityGroupNumber",
        description="Affinity Group Number",
    )
    vrf_range: Union[Variable, Global[str], Default[None]] = Field(
        default=as_default(None),
        serialization_alias="vrfRange",
        validation_alias="vrfRange",
        description="Range of VRFs",
    )


class BasicParcel(_ParcelBase):
    type_: Literal["basic"] = Field(default="basic", exclude=True)

    model_config = ConfigDict(
        extra="forbid",
    )
    clock: Clock
    description: Union[Variable, Global[str], Default[None]] = Field(
        default=as_default(None), description="Set a text description of the device"
    )
    location: Union[Variable, Global[str], Default[None]] = Field(
        default=as_default(None), description="Set the location of the device"
    )
    gps_location: GpsVariable = Field(
        ...,
        serialization_alias="gpsVariable",
        validation_alias="gpsVariable",
    )
    device_groups: Union[Variable, Global[List[str]], Default[None]] = Field(
        default=as_default(None),
        serialization_alias="deviceGroups",
        validation_alias="deviceGroups",
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
        serialization_alias="controllerGroupList",
        validation_alias="controllerGroupList",
        description="Configure a list of comma-separated controller groups",
    )
    overlay_id: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(1),
        serialization_alias="overlayId",
        validation_alias="overlayId",
        description="Set the Overlay ID",
    )
    port_offset: Union[Variable, Global[int], Default[int]] = Field(
        default=as_default(0),
        serialization_alias="portOffset",
        validation_alias="portOffset",
        description="Set the TLOC port offset when multiple devices are behind a NAT",
    )
    port_hop: Union[Variable, Global[bool], Default[Literal[True]]] = Field(
        default=True,
        serialization_alias="portHop",
        validation_alias="portHop",
        description="Enable port hopping",
    )
    control_session_pps: Optional[Union[Variable, Global[int], Default[int]]] = Field(
        None,
        serialization_alias="controlSessionPps",
        validation_alias="controlSessionPps",
        description="Set the policer rate for control sessions",
    )
    track_transport: Optional[Union[Variable, Global[bool], Default[Literal[True]]]] = Field(
        None,
        serialization_alias="trackTransport",
        validation_alias="trackTransport",
        description="Configure tracking of transport",
    )
    track_interface_tag: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        None,
        serialization_alias="trackInterfaceTag",
        validation_alias="trackInterfaceTag",
        description="OMP Tag attached to routes based on interface tracking",
    )
    console_baud_rate: Union[Variable, Global[ConsoleBaudRate], Default[DefaultConsoleBaudRate]] = Field(
        default=as_default("9600"),
        serialization_alias="consoleBaudRate",
        validation_alias="consoleBaudRate",
        description="Set the console baud rate",
    )
    max_omp_sessions: Union[Variable, Global[int], Default[None]] = Field(
        default=as_default(None),
        serialization_alias="maxOmpSessions",
        validation_alias="maxOmpSessions",
        description="Set the maximum number of OMP sessions <1..100> the device can have",
    )
    multi_tenant: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        None,
        serialization_alias="multiTenant",
        validation_alias="multiTenant",
        description="Device is multi-tenant",
    )
    track_default_gateway: Optional[
        Union[
            Variable,
            Global[bool],
            Default[Literal[True]],
        ]
    ] = Field(
        None,
        serialization_alias="trackDefaultGateway",
        validation_alias="trackDefaultGateway",
        description="Enable or disable default gateway tracking",
    )
    tracker_dia_stabilize_status: Optional[
        Union[
            Variable,
            Global[bool],
            Default[Literal[False]],
        ]
    ] = Field(
        None,
        serialization_alias="trackerDiaStabilizeStatus",
        validation_alias="trackerDiaStabilizeStatus",
        description="Enable or disable endpoint tracker diaStabilize status",
    )
    admin_tech_on_failure: Union[Variable, Global[bool], Default[Literal[True]]] = Field(
        default=as_default(True),
        serialization_alias="adminTechOnFailure",
        validation_alias="adminTechOnFailure",
        description="Collect admin-tech before reboot due to daemon failure",
    )
    idle_timeout: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        None,
        serialization_alias="idleTimeout",
        validation_alias="idleTimeout",
        description="Idle CLI timeout in minutes",
    )
    on_demand: OnDemand = Field(
        ...,
        serialization_alias="onDemand",
        validation_alias="onDemand",
    )
    transport_gateway: Optional[Union[Global[bool], Variable, Default[Literal[False]]]] = Field(
        None,
        serialization_alias="transportGateway",
        validation_alias="transportGateway",
        description="Enable transport gateway",
    )
    epfr: Optional[Union[Global[Epfr], Default[DefaultEpfr], Variable]] = Field(
        None,
        description="Enable SLA Dampening and Enhanced App Routing.",
    )
    site_type: Optional[Union[Variable, Global[List[SiteType]], Default[None]]] = Field(
        None,
        serialization_alias="siteType",
        validation_alias="siteType",
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
        serialization_alias="affinityGroupGlobal[str]",
        validation_alias="affinityGroupGlobal[str]",
        description="Affinity Group Global[str]",
    )
    affinity_group_preference: Optional[
        Union[
            Variable,
            Global[List[int]],
            Default[None],
        ]
    ] = Field(
        None,
        serialization_alias="affinityGroupPreference",
        validation_alias="affinityGroupPreference",
        description="Affinity Group Preference",
    )
    affinity_preference_auto: Optional[
        Union[
            Variable,
            Global[bool],
            Default[Literal[False]],
        ]
    ] = Field(
        None,
        serialization_alias="affinityPreferenceAuto",
        validation_alias="affinityPreferenceAuto",
        description="Affinity Group Preference Auto",
    )
    affinity_per_vrf: Optional[List[AffinityPerVrfItem]] = Field(
        None,
        serialization_alias="affinityPerVrf",
        validation_alias="affinityPerVrf",
        description="Affinity Group Global[str] for VRFs",
        max_length=4,
        min_length=0,
    )
