from pydantic import BaseModel


class DeviceVariable(BaseModel):
    name: str
