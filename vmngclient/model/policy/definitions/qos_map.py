from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator

from vmngclient.model.policy.policy_definition import PolicyDefinitionHeader


class QoSSchedulingEnum(str, Enum):
    LLQ = "llq"
    WRR = "wrr"


class QoSDropEnum(str, Enum):
    TAIL = "tail-drop"
    RANDOM_EARLY = "red-drop"


class QoSScheduler(BaseModel):
    queue: str
    class_map_ref: str = Field(alias="classMapRef")
    bandwidth_percent: str = Field("1", alias="bandwidthPercent")
    buffer_percent: str = Field("1", alias="bufferPercent")
    burst: Optional[str] = None
    scheduling: QoSSchedulingEnum = QoSSchedulingEnum.WRR
    drops: QoSDropEnum = QoSDropEnum.TAIL
    temp_key_values: Optional[str] = Field(None, alias="tempKeyValues")

    @staticmethod
    def get_default_control_scheduler() -> "QoSScheduler":
        return QoSScheduler(  # type: ignore[call-arg]
            queue="0",
            class_map_ref="",
            bandwidth_percent="100",
            buffer_percent="100",
            burst="15000",
            scheduling=QoSSchedulingEnum.LLQ,
            drops=QoSDropEnum.TAIL,
        )

    class Config:
        allow_population_by_field_name = True

    @validator("queue")
    def check_queue(cls, queue_str: str):
        queue = int(queue_str)
        if queue < 0 or queue > 7:
            raise ValueError("queue should be in range 0-7")
        return queue_str

    @validator("bandwidth_percent", "buffer_percent")
    def check_bandwidth_and_buffer_percent(cls, percent_str: str):
        percent = int(percent_str)
        if percent < 1 or percent > 100:
            raise ValueError("bandwidth/buffer percent should be in range 1-100")
        return percent_str

    @validator("burst")
    def check_burst(cls, burst_val: Union[str, None]):
        if burst_val is not None:
            burst = int(burst_val)
            if burst < 5000 or burst > 10_000_000:
                raise ValueError("burst should be in range 5000-10000000")
        return burst_val


class QoSMapDefinition(BaseModel):
    qos_schedulers: List[QoSScheduler] = Field(alias="qosSchedulers")

    class Config:
        allow_population_by_field_name = True


class QoSMap(PolicyDefinitionHeader):
    type: str = Field(default="qosMap", const=True)
    definition: QoSMapDefinition = QoSMapDefinition(qosSchedulers=[])

    class Config:
        allow_population_by_field_name = True

    def add_scheduler(
        self,
        queue: int,
        class_map_ref: str,
        bandwidth: int = 1,
        buffer: int = 1,
        scheduling: QoSSchedulingEnum = QoSSchedulingEnum.WRR,
        drops: QoSDropEnum = QoSDropEnum.TAIL,
        burst: Optional[int] = None,
    ) -> None:
        self.definition.qos_schedulers.append(
            QoSScheduler(  # type: ignore[call-arg]
                queue=str(queue),
                class_map_ref=class_map_ref,
                bandwidth_percent=str(bandwidth),
                buffer_percent=str(buffer),
                burst=str(burst) if burst is not None else None,
                scheduling=scheduling,
                drops=drops,
            )
        )

    @root_validator  # type: ignore[call-overload]
    def generate_default_control_scheduler(cls, values) -> Dict:
        definition: QoSMapDefinition = values.get("definition")
        if not definition.qos_schedulers:
            # Only when creating (not when value obtained from remote is present)
            values["definition"] = QoSMapDefinition(  # type: ignore[call-arg]
                qos_schedulers=[QoSScheduler.get_default_control_scheduler()]
            )
        return values
