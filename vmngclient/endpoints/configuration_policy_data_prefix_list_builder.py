# mypy: disable-error-code="empty-body"
from ipaddress import IPv4Network
from typing import List

from pydantic import BaseModel, Field, validator

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy_list import InfoTag, PolicyList, PolicyListId, PolicyListInfo, PolicyListPreview
from vmngclient.typed_list import DataSequence


class DataPrefixListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    ip_prefix: str = Field(alias="ipPrefix", description="IP4 network prefixes separated by comma")

    @validator("ip_prefix")
    def check_network_prefixes(cls, ip_prefix: str):
        nets = [IPv4Network(net.strip()) for net in ip_prefix.split(",")]
        if len(nets) < 1:
            raise ValueError("No network prefix provided")
        return ip_prefix


class DataPrefixList(PolicyList):
    entries: List[DataPrefixListEntry]
    type: str = Field(default="dataPrefix", const=True)


class DataPrefixListEditPayload(DataPrefixList, PolicyListId):
    pass


class DataPrefixListInfo(DataPrefixList, PolicyListInfo):
    pass


class ConfigurationPolicyDataPrefixListBuilder(APIEndpoints):
    @post("/template/policy/list/dataprefix")
    def create_policy_list(self, payload: DataPrefixList) -> PolicyListId:
        ...

    @delete("/template/policy/list/dataprefix/{id}")
    def delete_policy_list(self, id: str) -> None:
        ...

    @delete("/template/policy/list/dataprefix")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/dataprefix/{id}")
    def edit_policy_list(self, id: str, payload: DataPrefixListEditPayload) -> None:
        ...

    @get("/template/policy/list/dataprefix/{id}")
    def get_lists_by_id(self, id: str) -> DataPrefixListInfo:
        ...

    @get("/template/policy/list/dataprefix", "data")
    def get_policy_lists(self) -> DataSequence[DataPrefixListInfo]:
        ...

    @get("/template/policy/list/dataprefix/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[DataPrefixListInfo]:
        ...

    @post("/template/policy/list/dataprefix/preview")
    def preview_policy_list(self, payload: DataPrefixList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/dataprefix/preview/{id}")
    def preview_policy_list_by_id(self, id: str) -> PolicyListPreview:
        ...
