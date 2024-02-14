from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class CriteriaEnum(str, Enum):
    LOSS = "loss"
    LATENCY = "latency"
    JITTER = "jitter"
    LOSS_LATENCY = "loss-latency"
    LOSS_JITTER = "loss-jitter"
    LATENCY_LOSS = "latency-loss"
    LATENCY_JITTER = "latency-jitter"
    JITTER_LATENCY = "jitter-latency"
    JITTER_LOSS = "jitter-loss"
    LOSS_LATENCY_JITTER = "loss-latency-jitter"
    LOSS_JITTER_LATENCY = "loss-jitter-latency"
    LATENCY_LOSS_JITTER = "latency-loss-jitter"
    LATENCY_JITTER_LOSS = "latency-jitter-loss"
    JITTER_LATENCY_LOSS = "jitter-latency-loss"
    JITTER_LOSS_LATENCY = "jitter-loss-latency"


class Latency(Global):
    value: int = Field(ge=1, le=1000)


class Loss(Global):
    value: int = Field(ge=0, le=100)


class Jitter(Global):
    value: int = Field(ge=1, le=1000)


class LatencyVariance(Latency):
    ...


class LossVariance(Loss):
    ...


class JitterVariance(Jitter):
    ...


class AppProbeClass(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ref_id: Global[UUID] = Field(serialization_alias="refId", validation_alias="refId")


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: Global[CriteriaEnum]
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

    def add_criterias(
        self, jitter_variance: Union[int, None], latency_variance: Union[int, None], loss_variance: Union[int, None]
    ):
        expected_criterias = []
        if jitter_variance:
            self.jitter_variance = JitterVariance(value=jitter_variance)
            expected_criterias.append("jitter")
        if latency_variance:
            self.latency_variance = LatencyVariance(value=latency_variance)
            expected_criterias.append("latency")
        if loss_variance:
            self.loss_variance = LossVariance(value=loss_variance)
            expected_criterias.append("loss")
        for e in expected_criterias:
            if e not in self.criteria.value:
                raise ValueError(f"Criteria {e} is not in configured criteraias {self.criteria.value}")

    @field_validator("latency_variance")
    @classmethod
    def check_latency(cls, latency: Global):
        assert 1 <= latency.value <= 1000
        return latency

    @field_validator("loss_variance")
    @classmethod
    def check_loss(cls, loss: Global):
        assert 0 <= loss.value <= 100
        return loss

    @field_validator("jitter_variance")
    @classmethod
    def check_jitter(cls, jitter: Global):
        assert 1 <= jitter.value <= 1000
        return jitter


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[Global[int]] = None
    loss: Optional[Global[int]] = None
    jitter: Optional[Global[int]] = None
    app_probe_class: Optional[AppProbeClass] = Field(
        validation_alias="appProbeClass", serialization_alias="appProbeClass"
    )
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(
        default=None, validation_alias="fallbackBestTunnel", serialization_alias="fallbackBestTunnel"
    )

    @field_validator("latency")
    @classmethod
    def check_latency(cls, latency: Global):
        assert 1 <= latency.value <= 1000
        return latency

    @field_validator("loss")
    @classmethod
    def check_loss(cls, loss: Global):
        assert 0 <= loss.value <= 100
        return loss

    @field_validator("jitter")
    @classmethod
    def check_jitter(cls, jitter: Global):
        assert 1 <= jitter.value <= 1000
        return jitter


class SLAClassParcel(_ParcelBase):
    entries: List[SLAClassListEntry] = Field(validation_alias=AliasPath("data", "entries"))
