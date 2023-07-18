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
    try:
        parsed_version = Version(version)
        return Version(f"{parsed_version.major}.{parsed_version.minor}")
    except InvalidVersion:
        try:
            parsed_version = Version(".".join(version.split(".")[:2]))
            return Version(f"{parsed_version.major}.{parsed_version.minor}")
        except InvalidVersion:
            return NullVersion()
