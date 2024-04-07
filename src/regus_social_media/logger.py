import logging
from src.exceptions.logger import (
    LoggerInvalidLevelException,
    LoggerInvalidNameException,
)


class CustomLogger:
    """
    Class with methods to create a custom logger
    and contains the following methods
    - _validate_logger: validates the logger name and level
    - _create_formatter: creates a custom formatter for the logger
    - _create_handler: creates a custom handler for the logger
    - create_logger: creates a custom logger
    - return_logger: returns the custom logger
    """

    def __init__(self, logger_name: str, logger_level: int):
        self.logger_name = logger_name
        self.logger_level = logger_level

    def _validate_logger(self):
        if not isinstance(self.logger_name, str):
            raise LoggerInvalidNameException("Logger name is required")
        if len(self.logger_name) == 0:
            raise LoggerInvalidNameException("Logger name is required")

        if self.logger_level not in [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]:
            raise LoggerInvalidLevelException("Logger level is required")

    def _create_formatter(self):
        self._validate_logger
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _create_handler(self):
        self._validate_logger
        handler = logging.StreamHandler()
        handler.setFormatter(self._create_formatter())
        return handler

    def create_logger(self):
        self._validate_logger
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logger_level)
        logger.handlers.clear()
        logger.addHandler(self._create_handler())
        self.logger = logger

    def return_logger(self):
        self.create_logger()
        return self.logger
