# Copyright 2022 Cisco Systems, Inc. and its affiliates

import logging
import logging.config
import multiprocessing
from functools import lru_cache, wraps
from importlib import metadata
from importlib.machinery import PathFinder
from os import environ
from pathlib import Path
from traceback import FrameSummary, StackSummary, extract_stack
from typing import Callable, Final, List, Optional

import urllib3

USER_AGENT = f"{__package__}/{metadata.version(__package__)}"


def with_proc_info_header(method: Callable[..., str]) -> Callable[..., str]:
    """
    Adds process ID and external caller information before first line of returned string
    """

    @wraps(method)
    def wrapper(*args, **kwargs) -> str:
        wrapped = method(*args, **kwargs)
        header = f"{multiprocessing.current_process()}"
        if frame_summary := get_first_external_stack_frame(extract_stack()):
            fname, line_no, function, _ = frame_summary
            header += " %s:%d %s(...)" % (fname, line_no, function)
        header += "\n"
        return header + wrapped

    return wrapper


def get_first_external_stack_frame(stack: StackSummary) -> Optional[FrameSummary]:
    """
    Get the first python frame
    on the stack before entering catalystwan module
    """
    if len(stack) < 1:
        return None
    for index, frame in enumerate(stack):
        if is_file_in_package(frame.filename):
            break
    if index == 0:
        return None
    return stack[index - 1]


@lru_cache()
def is_file_in_package(fname: str) -> bool:
    """
    Checks if filepath given by string
    is part of catalystwan source code
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


if environ.get("catalystwan_devel") is not None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    catalystwan_logger = logging.getLogger(__name__)
    logging.config.fileConfig(LOGGING_CONF_DIR, disable_existing_loggers=False)
    catalystwan_logger.debug(f"catalystwan {__version__}")
