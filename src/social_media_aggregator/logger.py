import logging
from .exceptions.logger import LoggerInvalidArguments, LoggerInvalidLevelException
from .helpers.helpers import validate_arguments


class CustomLogger:
    """
    Class with methods to create a custom logger
    and contains the following methods:
    - _validate_logger: validates the logger name and level
    - _create_formatter: creates a custom formatter for the logger
    - _create_handler: creates a custom handler for the logger
    - create_logger: creates a custom logger
    - return_logger: returns the custom logger
    """

    @validate_arguments(
        (str, True), (int, True), exception_class=LoggerInvalidArguments
    )
    def __init__(self, logger_name: str, logger_level: int):
        self.logger_name = logger_name
        self.logger_level = logger_level

    def _create_formatter(self):
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _create_handler(self):
        handler = logging.StreamHandler()
        handler.setFormatter(self._create_formatter())
        return handler

    def create_logger(self):
        if self.logger_level not in [
            logging.CRITICAL,
            logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
        ]:
            raise LoggerInvalidLevelException(
                f"Argument 'logger_level' with value '{self.logger_level}' is not a valid logging level."
            )

        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logger_level)
        logger.handlers.clear()
        logger.addHandler(self._create_handler())
        self.logger = logger

    def return_logger(self):
        self.create_logger()
        return self.logger
