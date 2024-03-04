# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from catalystwan.endpoints import APIEndpointClient, APIEndpoints, get
from catalystwan.models.misc.application_protocols import ApplicationProtocolMap
from catalystwan.typed_list import DataSequence


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
