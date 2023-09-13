# mypy: disable-error-code="empty-body"
from typing import List

from pydantic import BaseModel, Field, validator

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy_list import (
    InfoTag,
    PolicyList,
    PolicyListCreationPayload,
    PolicyListEditPayload,
    PolicyListId,
    PolicyListPreview,
)
from vmngclient.typed_list import DataSequence


class VPNListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    vpn: str = Field(alias="vpn", description="0-65530 range or single number")

    @validator("vpn")
    def check_vpn_range(cls, vpns_str: str):
        vpns = [int(vpn) for vpn in vpns_str.split("-")]
        if len(vpns) > 2:
            raise ValueError("VPN range should consist two integers separated by hyphen")
        for vpn in vpns:
            if vpn < 0 or vpn > 65530:
                raise ValueError("VPN should be in range 0-65530")
        if len(vpns) == 2 and vpns[0] >= vpns[1]:
            raise ValueError("Second VPN in range should be greater than first")
        return vpns_str


class VPNPayload(BaseModel):
    entries: List[VPNListEntry]
    type: str = Field(default="vpn", const=True)


class VPNListCreationPayload(VPNPayload, PolicyListCreationPayload):
    pass


class VPNListEditPayload(VPNPayload, PolicyListEditPayload):
    pass


class VPNList(VPNPayload, PolicyList):
    pass


class ConfigurationPolicyVPNListBuilder(APIEndpoints):
    @post("/template/policy/list/vpn")
    def create_policy_list(self, payload: VPNListCreationPayload) -> PolicyListId:
        ...

    @delete("/template/policy/list/vpn/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/vpn")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        # TODO: dont know how to assing tags to check if filter works
        # (it is present in GET response but cannot be added to POST, PUT payload)
        # for now it was tested with default info tag value == ""
        ...

    @put("/template/policy/list/vpn/{id}")
    def edit_policy_list(self, id: str, payload: VPNListEditPayload) -> None:
        ...

    @get("/template/policy/list/vpn/{id}")
    def get_lists_by_id(self, id: str) -> VPNList:
        ...

    @get("/template/policy/list/vpn", "data")
    def get_policy_lists(self) -> DataSequence[VPNList]:
        ...

    @get("/template/policy/list/vpn/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[VPNList]:
        # TODO: dont know how to assing tags to check if filter works
        # (it is present in GET response but cannot be added to POST, PUT payload)
        # for now it was tested with default info tag value == ""
        ...

    @post("/template/policy/list/vpn/preview")
    def preview_policy_list(self, payload: VPNListCreationPayload) -> PolicyListPreview:
        ...

    @get("/template/policy/list/vpn/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
