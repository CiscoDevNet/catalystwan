# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


def check_jitter_ms(jitter_str: Optional[str]) -> Optional[str]:
    if jitter_str is not None:
        assert 1 <= int(jitter_str) <= 1000
    return jitter_str


def check_latency_ms(latency_str: Optional[str]) -> Optional[str]:
    if latency_str is not None:
        assert 1 <= int(latency_str) <= 1000
    return latency_str


def check_loss_percent(loss_str: Optional[str]) -> Optional[str]:
    if loss_str is not None:
        assert 0 <= int(loss_str) <= 100
    return loss_str


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: str
    jitter_variance: Optional[str] = Field(
        default=None,
        serialization_alias="jitterVariance",
        validation_alias="jitterVariance",
        description="jitter variance in ms",
    )
    latency_variance: Optional[str] = Field(
        default=None,
        serialization_alias="latencyVariance",
        validation_alias="latencyVariance",
        description="latency variance in ms",
    )
    loss_variance: Optional[str] = Field(
        default=None,
        serialization_alias="lossVariance",
        validation_alias="lossVariance",
        description="loss variance as percentage",
    )
    _criteria_priority: List[Literal["jitter", "latency", "loss"]] = []

    # validators
    _jitter_validator = field_validator("jitter_variance")(check_jitter_ms)
    _latency_validator = field_validator("latency_variance")(check_latency_ms)
    _loss_validator = field_validator("loss_variance")(check_loss_percent)

    @model_validator(mode="after")
    def check_criteria(self):
        expected_criteria = set()
        if self.jitter_variance is not None:
            expected_criteria.add("jitter")
        if self.latency_variance is not None:
            expected_criteria.add("latency")
        if self.loss_variance is not None:
            expected_criteria.add("loss")
        assert expected_criteria, "At least one variance type needs to be present"
        self._criteria_priority = str(self.criteria).split("-")
        observed_criteria = set(self._criteria_priority)
        assert expected_criteria == observed_criteria
        return self

    def _update_criteria_field(self) -> None:
        self.criteria = f"{'-'.join(self._criteria_priority)}"

    def add_jitter_criteria(self, jitter_variance: int) -> None:
        if self.jitter_variance is None:
            self._criteria_priority.append("jitter")
        self.jitter_variance = str(jitter_variance)
        self._update_criteria_field()
        self.check_criteria

    def add_latency_criteria(self, latency_variance: int) -> None:
        if self.latency_variance is None:
            self._criteria_priority.append("latency")
        self.latency_variance = str(latency_variance)
        self._update_criteria_field()
        self.check_criteria

    def add_loss_criteria(self, loss_variance: int) -> None:
        if self.loss_variance is None:
            self._criteria_priority.append("loss")
        self.loss_variance = str(loss_variance)
        self._update_criteria_field()
        self.check_criteria


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[str] = None
    loss: Optional[str] = None
    jitter: Optional[str] = None
    app_probe_class: Optional[UUID] = Field(
        default=None, serialization_alias="appProbeClass", validation_alias="appProbeClass"
    )
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(
        default=None, serialization_alias="fallbackBestTunnel", validation_alias="fallbackBestTunnel"
    )

    # validators
    _jitter_validator = field_validator("jitter")(check_jitter_ms)
    _latency_validator = field_validator("latency")(check_latency_ms)
    _loss_validator = field_validator("loss")(check_loss_percent)

    @model_validator(mode="after")
    def check_at_least_one_criteria_is_set(self):
        assert any([self.latency, self.loss, self.jitter])
        return self

    def add_fallback_jitter_criteria(self, jitter_variance: int) -> None:
        if self.fallback_best_tunnel:
            self.fallback_best_tunnel.add_jitter_criteria(jitter_variance)
        else:
            self.fallback_best_tunnel = FallbackBestTunnel(criteria="jitter", jitter_variance=str(jitter_variance))

    def add_fallback_latency_criteria(self, latency_variance: int) -> None:
        if self.fallback_best_tunnel:
            self.fallback_best_tunnel.add_latency_criteria(latency_variance)
        else:
            self.fallback_best_tunnel = FallbackBestTunnel(criteria="latency", latency_variance=str(latency_variance))

    def add_fallback_loss_criteria(self, loss_variance: int) -> None:
        if self.fallback_best_tunnel:
            self.fallback_best_tunnel.add_loss_criteria(loss_variance)
        else:
            self.fallback_best_tunnel = FallbackBestTunnel(criteria="loss", loss_variance=str(loss_variance))


class SLAClassList(PolicyListBase):
    type: Literal["sla"] = "sla"
    entries: List[SLAClassListEntry] = []

    def assign_app_probe_class(
        self,
        app_probe_class_id: UUID,
        latency: Optional[int] = None,
        loss: Optional[int] = None,
        jitter: Optional[int] = None,
    ) -> SLAClassListEntry:
        # SLA class list must have only one entry!
        _latency = str(latency) if latency is not None else None
        _loss = str(loss) if loss is not None else None
        _jitter = str(jitter) if jitter is not None else None
        entry = SLAClassListEntry(latency=_latency, loss=_loss, jitter=_jitter, app_probe_class=app_probe_class_id)
        self._add_entry(entry, single=True)
        return entry

    def add_fallback_jitter_criteria(self, jitter_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_jitter_criteria(jitter_variance)

    def add_fallback_latency_criteria(self, latency_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_latency_criteria(latency_variance)

    def add_fallback_loss_criteria(self, loss_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_loss_criteria(loss_variance)


class SLAClassListEditPayload(SLAClassList, PolicyListId):
    pass


class SLAClassListInfo(SLAClassList, PolicyListInfo):
    pass
