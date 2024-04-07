import pytest
import logging
from exceptions.meta import (
    MetaInvalidEndpointException,
    MetaInvalidTokenException,
    MetaApiException,
)
from scripts.logger import CustomLogger
from scripts.meta import Meta


def test_invalid_api_endpoint_1():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(logger=logger, meta_url="", api_key="test")
    with pytest.raises(MetaInvalidEndpointException) as e:
        meta._validate_arguments()
    assert str(e.value) == "Meta error. API endpoint is required"


def test_invalid_api_endpoint_2():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(logger=logger, meta_url=None, api_key="test")
    with pytest.raises(MetaInvalidEndpointException) as e:
        meta._validate_arguments()
    assert str(e.value) == "Meta error. API endpoint is required"


def test_invalid_api_key_1():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(logger=logger, meta_url="test", api_key="")
    with pytest.raises(MetaInvalidTokenException) as e:
        meta._validate_arguments()
    assert str(e.value) == "Meta error. API key is required"


def test_invalid_api_key_2():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(logger=logger, meta_url="test", api_key=None)
    with pytest.raises(MetaInvalidTokenException) as e:
        meta._validate_arguments()
    assert str(e.value) == "Meta error. API key is required"


def test_get_all_accounts_invalid_1():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger, meta_url="https://graph.facebook.com/v19.0", api_key="test"
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_accounts(api_endpoint="test")
    assert str(e.value) == "Meta error. API error occurred. Error 400: Bad Request"


def test_get_all_accounts_invalid_2():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger, meta_url="https://graph.facebook.com/v19.0", api_key="test"
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_accounts()
    assert str(e.value) == "Meta error. API error occurred. Error 400: Bad Request"
