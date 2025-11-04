import aiogram.loggers
import structlog


def wrap_loggers():
    loggers = "dispatcher", "event", "middlewares", "webhook", "scene"
    for logger in loggers:
        raw_logger = getattr(aiogram.loggers, logger)
        setattr(aiogram.loggers, logger, structlog.wrap_logger(raw_logger))
