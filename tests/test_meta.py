import pytest
import logging
import os
from src.social_media_aggregator.exceptions.meta import (
    MetaInvalidEndpointException,
    MetaInvalidTokenException,
    MetaApiException,
)
from src.social_media_aggregator.logger import CustomLogger
from src.social_media_aggregator.meta import Meta

sandbox_api_key = os.getenv("META_SANDBOX_API_KEY")
meta_api_key = os.getenv("META_API_KEY")


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
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=sandbox_api_key,
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_accounts(api_endpoint="test")
    assert (
        str(e.value)
        == "Meta error. API error occurred. Error 400: Bad Request. Meta error message: 'Unsupported get request. Object with ID 'test' does not exist, cannot be loaded due to missing permissions, or does not support this operation. Please read the Graph API documentation at https://developers.facebook.com/docs/graph-api'. Meta error type: 'GraphMethodException'"
    )


def test_get_all_accounts_invalid_2():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger, meta_url="https://graph.facebook.com/v19.0", api_key="test"
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_accounts()
    assert (
        str(e.value)
        == "Meta error. API error occurred. Error 400: Bad Request. Meta error message: 'Invalid OAuth access token - Cannot parse access token'. Meta error type: 'OAuthException'"
    )


def test_permissions_error():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=sandbox_api_key,
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_accounts(api_endpoint="act_257329590612540")
    assert (
        str(e.value)
        == "Meta error. API error occurred. Error 400: Bad Request. Meta error message: '(#100) Missing permissions'. Meta error type: 'OAuthException'"
    )


def test_valid_get_account():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    meta.get_accounts(api_endpoint="me/adaccounts")
    assert len(meta._all_accounts) > 0
