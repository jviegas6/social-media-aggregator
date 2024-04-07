import pytest
from src.regus_social_media.logger import CustomLogger
from src.exceptions.logger import (
    LoggerInvalidLevelException,
    LoggerInvalidNameException,
)


def test_invalid_logger_name_1():
    with pytest.raises(LoggerInvalidNameException) as e:
        CustomLogger(logger_name=1, logger_level=10)._validate_logger()
    assert str(e.value) == "Logger name is required"


def test_invalid_logger_name_2():
    with pytest.raises(LoggerInvalidNameException) as e:
        CustomLogger(logger_name="", logger_level=10)._validate_logger()
    assert str(e.value) == "Logger name is required"


def test_invalid_logger_level_1():
    with pytest.raises(LoggerInvalidLevelException) as e:
        CustomLogger(logger_name="test", logger_level=1)._validate_logger()
    assert str(e.value) == "Logger level is required"


def test_valid_logger():
    logger = CustomLogger(logger_name="test", logger_level=10).return_logger()
    assert logger.name == "test"
    assert logger.level == 10
