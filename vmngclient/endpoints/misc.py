# mypy: disable-error-code="empty-body"
from vmngclient.endpoints import APIEndpointClient, APIEndpoints, get
from vmngclient.model.misc.application_protocols import ApplicationProtocolMap
from vmngclient.typed_list import DataSequence


class MiscellaneousEndpoints(APIEndpoints):
    def __init__(self, client: APIEndpointClient):
        self._client = client
        self._basepath = ""

    @get("/app/json/application_protocol.json", "data")
    def get_application_protocols(self) -> DataSequence[ApplicationProtocolMap]:
        """Not in spec, provides protocol name to protocol/port number mapping

        Returns:
            DataSequence[ApplicationProtocolMap]
        """
        ...
