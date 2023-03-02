import logging
import logging.config
from importlib import metadata
from os import environ
from pathlib import Path
from typing import Final

import urllib3

LOGGING_CONF_DIR: Final[str] = str(Path(__file__).parents[0] / "logging.conf")
__version__ = metadata.version(__package__)

if environ.get("VMNGCLIENT_DEVEL") is not None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    vmngclient_logger = logging.getLogger(__name__)
    logging.config.fileConfig(LOGGING_CONF_DIR, disable_existing_loggers=False)
    vmngclient_logger.debug(f"vmngclient {__version__}")
