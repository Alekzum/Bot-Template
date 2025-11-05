import aiogram.loggers
import structlog
import logging


def wrap_loggers():
    loggers = dir(aiogram.loggers)
    for logger in loggers:
        raw_logger = getattr(aiogram.loggers, logger)
        if not isinstance(raw_logger, logging.Logger):
            continue
        setattr(aiogram.loggers, logger, structlog.wrap_logger(raw_logger))
