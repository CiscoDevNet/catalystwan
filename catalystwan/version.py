# Copyright 2023 Cisco Systems, Inc. and its affiliates

import re

from packaging._structures import NegativeInfinity  # type: ignore
from packaging.version import InvalidVersion, Version  # type: ignore


class NullVersion(Version):
    """Represents non-existing `Version` object.

    `NullVersion` instance is considered as the lowest possible version.
    Any other `Version` object will be considered greater than the `NullVersion`.
    """

    def __init__(self):
        """Initialize a NullVersion object."""
        super().__init__("0")
        self._key = (
            NegativeInfinity,
            NegativeInfinity,
            NegativeInfinity,
            NegativeInfinity,
            NegativeInfinity,
            NegativeInfinity,
        )

    def __str__(self) -> str:
        """A representation of the NullVersion for the user.
        >>> NullVersion()
        NullVersion
        """
        return "NullVersion"


def parse_vmanage_version(version: str) -> Version:
    """Parse vmanage version string which could contain custom prefixes and suffixes
    Currently not conforming versions could be found in:
    GET /client/server: '20.12.0-144-li'
    GET /device/action/software/images?imageType=software: 'smart-li-20.13.999-3077'
    Strategy is to iterate by removing potentially problematic part until version is parsed.
    This is temporary solution until custom versioning scheme will be implemented.

    >>> parse_vmanage_version('20.12.0-144-li')
    <Version('20.12.0.post144')>
    >>> parse_vmanage_version('li-20.13.999-3077')
    <Version('20.13.999.post3077')>
    >>> parse_vmanage_version('smart-li-20.13.999-3077')
    <Version('20.13.999.post3077')>
    >>> parse_vmanage_version('Not a version.')
    <class 'catalystwan.version.NullVersion'>

    Args:
        version (str): The version string to parse.

    Returns:
        Version
    """

    def numeric_only(version: str) -> str:
        if match := re.search(r"\d.*\d", version):
            return str(match[0])
        return ""

    for candidate in [version, numeric_only(version)]:
        try:
            return Version(candidate)
        except InvalidVersion:
            continue
    return NullVersion()


def parse_api_version(version: str) -> Version:
    """Parse the given version string.

    When version string is not a valid `Version`, it tries to cut off major and minor part only.
    If that does not work, it produces a `NullVersion` object.

    >>> parse_api_version("20")
    <Version('20.0')>
    >>> parse_api_version("20.12.0-111-xy")
    <Version('20.12')>
    >>> parse_api_version("Not a version.")
    <Version('NullVersion')>

    Args:
        version (str): The version string to parse.

    Returns:
        Version: A Version with supported `major` and `minor` properties.
    """
    parsed_version = parse_vmanage_version(version)
    if not isinstance(parsed_version, NullVersion):
        return Version(f"{parsed_version.major}.{parsed_version.minor}")
    return NullVersion()
