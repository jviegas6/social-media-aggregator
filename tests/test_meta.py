import pytest
import logging
from exceptions.meta import (
    MetaInvalidEndpointException,
    MetaInvalidTokenException,
    MetaApiException,
)
from scripts.logger import CustomLogger
from scripts.meta import Meta

sandbox_api_key = "EAAGPGOEaGdIBO0LZAq2fX2eX5f2zb6R1UzGbyzyWQmhd8QZARZAqQboLuk9cqUXCOY9LyelHXH2TbZB2XYYmoVuvbPWnqCbvXhsXZCaAAZCzGjtoEm3ByZBpxZCQ5m14uqC11xqyNnSSr6syRHZACZA5dPkemsr1e6S7OB9V1MgrF8Qbv7a6M2RoSInPj1GeePD1ZCj4eKalsOG"


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
        api_key="EAAGPGOEaGdIBOwGcXMsbcjIsnM0rOhoUKuQDl3ToJ1dmTFJZCSB8hs67jwfGihkzaADAiKZAFce3f02pjT8XStOO9dZC6RblAZBjTLbOFHH6w5mN55GuEVTCTbcrQuZBgolUvA79bNVNrPAg2n1TRwtNJLMyL4pgsldRA982jZAP3w3KZC6uXZAM2MDBbS7D6ZCC4AGlKbCQz",
    )
    meta.get_accounts(api_endpoint="me/adaccounts")
    assert len(meta._all_accounts) > 0
