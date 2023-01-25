import logging
import logging.config
from importlib import metadata
from pathlib import Path
from typing import Final

LOGGING_CONF_DIR: Final[str] = str(Path(__file__).parents[0] / "logging.conf")

vmngclient_logger = logging.getLogger(__name__)

if not vmngclient_logger.handlers:
    logging.config.fileConfig(LOGGING_CONF_DIR, disable_existing_loggers=False)

__version__ = metadata.version(__package__)

vmngclient_logger.debug(f"vmngclient {__version__}")
