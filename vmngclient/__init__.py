import logging
import logging.config
from functools import lru_cache
from importlib import metadata
from importlib.machinery import PathFinder
from os import environ
from pathlib import Path
from traceback import FrameSummary, StackSummary
from typing import Final, List

import urllib3


def get_first_external_stack_frame(stack: StackSummary) -> FrameSummary:
    """
    Get the first python frame
    on the stack before entering vmngclient module
    """
    for index, frame in enumerate(stack):
        if is_file_in_package(frame.filename):
            break
    return stack[index - 1]


@lru_cache()
def is_file_in_package(fname: str) -> bool:
    """
    Checks if filepath given by string
    is part of vmngclient source code
    """
    return Path(fname) in pkg_src_list


def list_package_sources() -> List[Path]:
    """
    Creates a list containing paths to all python source files
    for current package
    """
    pkg_srcs: List[Path] = []
    if pkg_spec := PathFinder.find_spec(__package__):
        if pkg_origin := pkg_spec.origin:
            pkg_srcs = list(Path(pkg_origin).parent.glob("**/*.py"))
    return pkg_srcs


LOGGING_CONF_DIR: Final[str] = str(Path(__file__).parents[0] / "logging.conf")
__version__ = metadata.version(__package__)
pkg_src_list = list_package_sources()


if environ.get("VMNGCLIENT_DEVEL") is not None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    vmngclient_logger = logging.getLogger(__name__)
    logging.config.fileConfig(LOGGING_CONF_DIR, disable_existing_loggers=False)
    vmngclient_logger.debug(f"vmngclient {__version__}")
