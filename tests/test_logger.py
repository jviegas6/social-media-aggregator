import pytest
from src.social_media_aggregator.logger import CustomLogger
from src.social_media_aggregator.exceptions.logger import (
    LoggerInvalidArguments,
    LoggerInvalidLevelException,
)


def test_invalid_logger_name_1():
    with pytest.raises(LoggerInvalidArguments) as e:
        CustomLogger(logger_name=1, logger_level=10)
    assert (
        str(e.value)
        == "Logger error. Argument 'logger_name' with value '1' is not of type <class 'str'>."
    )


def test_invalid_logger_name_2():
    with pytest.raises(LoggerInvalidArguments) as e:
        CustomLogger(logger_name="", logger_level=10)
    assert (
        str(e.value)
        == "Logger error. Argument 'logger_name' is a mandatory string but received an empty string."
    )


def test_invalid_logger_level_1():
    with pytest.raises(LoggerInvalidLevelException) as e:
        CustomLogger(logger_name="test", logger_level=1)
    assert (
        str(e.value)
        == "Logger error. Argument 'logger_level' with value '1' is not a valid logging level."
    )


def test_valid_logger():
    logger = CustomLogger(logger_name="test", logger_level=10).return_logger()
    assert logger.name == "test"
    assert logger.level == 10
