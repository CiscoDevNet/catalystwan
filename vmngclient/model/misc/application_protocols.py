from socket import getprotobyname
from typing import Dict, List, Optional

from pydantic.v1 import BaseModel


class ApplicationProtocolEntry(BaseModel):
    name: str


class ApplicationProtocol(BaseModel):
    name: str
    protocol: Optional[str] = None
    port: Optional[str] = None
    entries: Optional[List[ApplicationProtocolEntry]]

    def protocol_as_numbers(self) -> List[int]:
        if self.protocol:
            return [getprotobyname(p) for p in self.protocol.split(" ")]
        return []

    def protocol_as_string_of_numbers(self) -> str:
        return " ".join(str(p) for p in self.protocol_as_numbers())


class ApplicationProtocolMap(BaseModel):
    __root__: Dict[str, ApplicationProtocol]
