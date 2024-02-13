from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class ApplicationType(str, Enum):
    THREE_COM_AMP_3 = "3com-amp3"
    THREE_COM_TSMUX = "3com-tsmux"
    THREE_PC = "3pc"
    FOUR_CHAN = "4chan"
    FIFTY_EIGHT_CITY = "58-city"
    NINE_HUNDRED_FOURTEEN_C_G = "914c/g"
    NINE_PFS = "9pfs"
    ABC_NEWS = "abc-news"
    ACAP = "acap"
    ACAS = "acas"
    ACCESS_BUILDER = "accessbuilder"
    ACCESS_NETWORK = "accessnetwork"
    ACCU_WEATHER = "accuweather"
    ARC_NEMA = "arc-nema"
    ACTIVE_DIRECTORY = "activte-directory"
    ACTIVE_SYNC = "activesync"
    AD_CASH = "adcash"
    ADD_THIS = "addthis"
    ADOBE_SERVICES = "adobe-services"
    ADP = "adp"
    AD_WEEK = "adweek"
    AED_512 = "aed-512"
    AF_POVERTY_TCP = "afpovertytcp"
    AGENT_X = "agentx"
    AIRBNB = "airbnb"
    AIRPLAY = "airplay"
    AKAMAI = "akamai"
    ALIWANGWANG = "aliwangwang"
    ALLRECIPES = "allrecipes"
    ALPES = "alpes"


class AppliactionFamilyType(str, Enum):
    ...


class ApplicationList(Global):
    value: Union[str, ApplicationType]


class ApplicationFamilyList(Global):
    value: Union[str, AppliactionFamilyType]


class ApplicationListEntry(BaseModel):
    app_list: ApplicationList = Field(alias="app")


class ApplicationFamilyListEntry(BaseModel):
    app_list_family: ApplicationFamilyList = Field(alias="appFamily")


class ApplicationListData(BaseModel):
    entries = List[Union[ApplicationListEntry, ApplicationFamilyListEntry]]


class ApplicationListPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.APP_LIST)
    data = ApplicationListData
