class InvalidOperationError(Exception):
    """The exception that is thrown when a method call is invalid for the object's current state."""

    pass


class RetrieveIntervalOutOfRange(Exception):
    pass


class VersionDeclarationError(Exception):
    """The exception that is thrown in one of two below cases.
    1. User passes software image and version, at the same time.
    2. User doesn't passes any of them."""

    pass


class ImageNotInRepositoryError(Exception):
    """The exception that is thrown, if image is not in vManage images Repository"""

    pass
