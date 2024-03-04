# Copyright 2024 Cisco Systems, Inc. and its affiliates

from pydantic import PlainSerializer
from typing_extensions import Annotated

BoolStr = Annotated[bool, PlainSerializer(lambda x: str(x).lower(), return_type=str, when_used="json-unless-none")]
