import logging
import logging.config
from pathlib import Path
from typing import Final

LOGGING_CONF_DIR: Final[str] = str(Path(__file__).parents[0] / 'logging.conf')

logging.config.fileConfig(LOGGING_CONF_DIR, disable_existing_loggers=False)
