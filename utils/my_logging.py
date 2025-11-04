import structlog
import logging.handlers
import logging
import sys
import typing
import os


LOG_DIR = "logs"
LOG_FILE = "log.log"
LEVEL_INFO = (
    logging.DEBUG if len(sys.argv) >= 2 and sys.argv[1] == "--debug" else logging.INFO
)
LEVEL_WARNING = (
    logging.DEBUG
    if len(sys.argv) >= 2 and sys.argv[1] == "--debug"
    else logging.WARNING
)


def my_callsite_processor(
    inclide_filename=True, include_funcname=True, inclide_lineno=True
):
    def inner(logger, method_nam, event_dict):
        file_n, func_n, line_n = (
            event_dict.pop("filename", ""),
            event_dict.pop("func_name", ""),
            event_dict.pop("lineno", ""),
        )
        array = []
        if inclide_filename:
            array.append(file_n)
        if include_funcname:
            array.append(func_n)
        if inclide_lineno:
            array.append(line_n)
        args = tuple(array)
        event_dict["modline"] = ":".join(str(i) for i in args)
        return event_dict

    return inner


# TODO
def filter_my_callsite_processor(blacklist: typing.Iterable = ()):
    def inner(logger, method_name, event):
        if any(logger.name.startswith(x) for x in blacklist):
            event.pop("modline")
        return event
    return inner


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ],
        ),
        my_callsite_processor(include_funcname=False),
        filter_my_callsite_processor(["aiogram"]),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

stream_formatter = structlog.stdlib.ProcessorFormatter(
    processors=[
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.dev.ConsoleRenderer(),
    ],
)

file_formatter = structlog.stdlib.ProcessorFormatter(
    processors=[
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.JSONRenderer(),
    ],
)

stream_handler = logging.StreamHandler()
file_handler = logging.handlers.TimedRotatingFileHandler(
    LOG_DIR + os.sep + LOG_FILE, encoding="utf-8", when="w0"
)
tempfile_handler = logging.FileHandler(
    LOG_DIR + os.sep + "temp" + LOG_FILE, encoding="utf-8", mode="w"
)

stream_handler.setFormatter(stream_formatter)
file_handler.setFormatter(file_formatter)
tempfile_handler.setFormatter(file_formatter)

LEVEL = LEVEL_INFO
stream_handler.setLevel(LEVEL)
file_handler.setLevel(LEVEL)
tempfile_handler.setLevel(logging.DEBUG)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(stream_handler)
root_logger.addHandler(file_handler)
root_logger.addHandler(tempfile_handler)
root_logger = structlog.wrap_logger(root_logger)

logger = structlog.get_logger(__name__)

logger.debug("Started", custom_level=LEVEL)
logger.info("Started", custom_level=LEVEL)

MUTEDICT = {
    "httpx": LEVEL_WARNING,
    "handlers": LEVEL_WARNING,
    "asyncio": logging.ERROR,
    "aiosqlite": logging.WARNING,
    "httpcore": logging.WARNING,
    "aiogram": LEVEL_INFO,
    "aiogram_dialog": LEVEL_WARNING,
    "asurso_api": LEVEL_WARNING,
    "utils.my_aiosqlitestore": LEVEL_WARNING,
}

for name, level in MUTEDICT.items():
    logging.getLogger(name).setLevel(level)
