# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global

SLAClassCriteria = Literal[
    "loss",
    "latency",
    "jitter",
    "loss-latency",
    "loss-jitter",
    "latency-loss",
    "latency-jitter",
    "jitter-latency",
    "jitter-loss",
    "loss-latency-jitter",
    "loss-jitter-latency",
    "latency-loss-jitter",
    "latency-jitter-loss",
    "jitter-latency-loss",
    "jitter-loss-latency",
]


def check_latency_ms(cls, latency: Optional[Global]):
    if latency is not None:
        assert 1 <= latency.value <= 1000
        return latency


def check_loss_percent(cls, loss: Optional[Global]):
    if loss is not None:
        assert 0 <= loss.value <= 100
    return loss


def check_jitter_ms(cls, jitter: Optional[Global]):
    if jitter is not None:
        assert 1 <= jitter.value <= 1000
    return jitter


class SLAAppProbeClass(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ref_id: Global[UUID] = Field(serialization_alias="refId", validation_alias="refId")


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: Global[SLAClassCriteria]
    jitter_variance: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="jitterVariance",
        validation_alias="jitterVariance",
        description="jitter variance in ms",
    )
    latency_variance: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="latencyVariance",
        validation_alias="latencyVariance",
        description="latency variance in ms",
    )
    loss_variance: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="lossVariance",
        validation_alias="lossVariance",
        description="loss variance as percentage",
    )
    # validators
    _jitter_validator = field_validator("jitter_variance")(check_jitter_ms)
    _latency_validator = field_validator("latency_variance")(check_latency_ms)
    _loss_validator = field_validator("loss_variance")(check_loss_percent)

    def add_criteria(
        self, jitter_variance: Union[int, None], latency_variance: Union[int, None], loss_variance: Union[int, None]
    ):
        expected_criteria = []
        if jitter_variance:
            self.jitter_variance = Global(value=jitter_variance)
            expected_criteria.append("jitter")
        if latency_variance:
            self.latency_variance = Global(value=latency_variance)
            expected_criteria.append("latency")
        if loss_variance:
            self.loss_variance = Global(value=loss_variance)
            expected_criteria.append("loss")
        for e in expected_criteria:
            if e not in self.criteria.value:
                raise ValueError(f"Criteria {e} is not in configured criteria {self.criteria.value}")


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[Global[int]] = None
    loss: Optional[Global[int]] = None
    jitter: Optional[Global[int]] = None
    app_probe_class: Optional[SLAAppProbeClass] = Field(
        validation_alias="appProbeClass", serialization_alias="appProbeClass"
    )
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(
        default=None, validation_alias="fallbackBestTunnel", serialization_alias="fallbackBestTunnel"
    )

    # validators
    _jitter_validator = field_validator("jitter")(check_jitter_ms)
    _latency_validator = field_validator("latency")(check_latency_ms)
    _loss_validator = field_validator("loss")(check_loss_percent)


class SLAClassParcel(_ParcelBase):
    type_: Literal["sla-class"] = Field(default="sla-class", exclude=True)
    entries: List[SLAClassListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_entry(
        self,
        app_probe_class_id: UUID,
        loss: Optional[int] = None,
        jitter: Optional[int] = None,
        latency: Optional[int] = None,
    ):
        self.entries.append(
            SLAClassListEntry(
                app_probe_class=SLAAppProbeClass(ref_id=as_global(app_probe_class_id)),
                loss=as_global(loss) if loss is not None else None,
                jitter=as_global(jitter) if jitter is not None else None,
                latency=as_global(latency) if latency is not None else None,
            )
        )

    def add_fallback(
        self,
        criteria: SLAClassCriteria,
        jitter_variance: Optional[int] = None,
        latency_variance: Optional[int] = None,
        loss_variance: Optional[int] = None,
    ):
        fallback = FallbackBestTunnel(
            criteria=as_global(criteria, SLAClassCriteria),
            jitter_variance=as_global(jitter_variance) if jitter_variance is not None else None,
            latency_variance=as_global(latency_variance) if latency_variance is not None else None,
            loss_variance=as_global(loss_variance) if loss_variance is not None else None,
        )
        self.entries[0].fallback_best_tunnel = fallback
