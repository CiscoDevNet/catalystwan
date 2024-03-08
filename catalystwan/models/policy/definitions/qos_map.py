# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from catalystwan.models.policy.policy_definition import PolicyDefinitionBase

QoSScheduling = Literal[
    "llq",
    "wrr",
]

QoSDropType = Literal[
    "tail-drop",
    "red-drop",
]


class QoSScheduler(BaseModel):
    queue: str
    class_map_ref: Union[UUID, Literal[""]] = Field(serialization_alias="classMapRef", validation_alias="classMapRef")
    bandwidth_percent: str = Field("1", serialization_alias="bandwidthPercent", validation_alias="bandwidthPercent")
    buffer_percent: str = Field("1", serialization_alias="bufferPercent", validation_alias="bufferPercent")
    burst: Optional[str] = None
    scheduling: QoSScheduling = "wrr"
    drops: QoSDropType = "tail-drop"
    temp_key_values: Optional[str] = Field(
        default=None, serialization_alias="tempKeyValues", validation_alias="tempKeyValues"
    )

    @staticmethod
    def get_default_control_scheduler() -> "QoSScheduler":
        return QoSScheduler(
            queue="0",
            class_map_ref="",
            bandwidth_percent="100",
            buffer_percent="100",
            burst="15000",
            scheduling="llq",
            drops="tail-drop",
        )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("queue")
    @classmethod
    def check_queue(cls, queue_str: str):
        assert 0 <= int(queue_str) <= 7
        return queue_str

    @field_validator("bandwidth_percent", "buffer_percent")
    @classmethod
    def check_bandwidth_and_buffer_percent(cls, percent_str: str):
        assert 1 <= int(percent_str) <= 100
        return percent_str

    @field_validator("burst")
    @classmethod
    def check_burst(cls, burst_val: Union[str, None]):
        if burst_val is not None:
            assert 5000 <= int(burst_val) <= 10_000_000
        return burst_val


class QoSMapDefinition(BaseModel):
    qos_schedulers: List[QoSScheduler] = Field(serialization_alias="qosSchedulers", validation_alias="qosSchedulers")
    model_config = ConfigDict(populate_by_name=True)


class QoSMapPolicy(PolicyDefinitionBase):
    type: Literal["qosMap"] = "qosMap"
    definition: QoSMapDefinition = QoSMapDefinition(qos_schedulers=[])
    model_config = ConfigDict(populate_by_name=True)

    def add_scheduler(
        self,
        queue: int,
        class_map_ref: UUID,
        bandwidth: int = 1,
        buffer: int = 1,
        scheduling: QoSScheduling = "wrr",
        drops: QoSDropType = "tail-drop",
        burst: Optional[int] = None,
    ) -> None:
        self.definition.qos_schedulers.append(
            QoSScheduler(
                queue=str(queue),
                class_map_ref=class_map_ref,
                bandwidth_percent=str(bandwidth),
                buffer_percent=str(buffer),
                burst=str(burst) if burst is not None else None,
                scheduling=scheduling,
                drops=drops,
            )
        )

    @model_validator(mode="after")
    def generate_default_control_scheduler(self):
        if not self.definition.qos_schedulers:
            # Only when creating (not when value obtained from remote is present)
            self.definition = QoSMapDefinition(qos_schedulers=[QoSScheduler.get_default_control_scheduler()])
        return self
