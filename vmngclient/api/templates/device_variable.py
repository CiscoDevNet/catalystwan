from pydantic.v1 import BaseModel


class DeviceVariable(BaseModel):
    name: str
