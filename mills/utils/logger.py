import logging
import os
from loguru import logger


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(
            depth=6, exception=record.exc_info, ansi=True, lazy=True
        )
        logger_opt.log(self._get_level(record), record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
log = logging.getLogger(__name__)
TelethonLogger = logging.getLogger("Telethon")
TelethonLogger.setLevel("INFO")


if os.path.exists('millie.log'):
    os.remove('millie.log')


logger.add(
    "millie.log",
    format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    rotation="7 days",
    compression="tar.xz",
    backtrace=True,
    diagnose=True,
    level="INFO",
    colorize=True,
)

log.info(f"Enabled logging intro userver.log file.")