import pytest
import logging
import os
from src.social_media_aggregator.exceptions.meta import (
    MetaInvalidArguments,
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
    with pytest.raises(MetaInvalidArguments) as e:
        Meta(logger=logger, meta_url="", api_key="test")
    assert (
        str(e.value)
        == "Meta error. Argument 'meta_url' is a mandatory string but received an empty string."
    )


def test_invalid_api_endpoint_2():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    with pytest.raises(MetaInvalidArguments) as e:
        Meta(logger=logger, meta_url=None, api_key="test")
    assert (
        str(e.value)
        == "Meta error. Argument 'meta_url' is mandatory but received None."
    )


def test_invalid_api_endpoint_3():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    with pytest.raises(MetaInvalidArguments) as e:
        Meta(logger=logger, meta_url="None", api_key=2)
    assert (
        str(e.value)
        == "Meta error. Argument 'api_key' with value '2' is not of type <class 'str'>."
    )


# def test_invalid_api_key_1():
#     logger = CustomLogger(
#         logger_level=logging.DEBUG, logger_name="test"
#     ).return_logger()
#     meta = Meta(logger=logger, meta_url="test", api_key="")
#     with pytest.raises(MetaInvalidTokenException) as e:
#         meta._validate_arguments()
#     assert str(e.value) == "Meta error. API key is required"


# def test_invalid_api_key_2():
#     logger = CustomLogger(
#         logger_level=logging.DEBUG, logger_name="test"
#     ).return_logger()
#     meta = Meta(logger=logger, meta_url="test", api_key=None)
#     with pytest.raises(MetaInvalidTokenException) as e:
#         meta._validate_arguments()
#     assert str(e.value) == "Meta error. API key is required"


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
        meta.get_accounts(api_endpoint="me/adaccounts")
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


def test_invalid_get_account_details_error_level():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_account_details(api_endpoint="act_2573295906125403", level="test")
    assert (
        str(e.value)
        == "Meta error. API error occurred. Error 400: Bad Request. Meta error message: '(#100) Param level must be one of {delivery_ad, politicalad, ad, adset, campaign, account}'. Meta error type: 'OAuthException'"
    )


def test_invalid_get_account_details_error_fields_list():
    fields_list = ["test", "test2"]
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_account_details(
            api_endpoint="act_2573295906125403", level="ad", fields_list=fields_list
        )
    assert (
        str(e.value)
        == f"Meta error. API error occurred. Error 400: Bad Request. Meta error message: '(#100) {', '.join(fields_list)} {'is' if len(fields_list) == 1 else 'are'} not valid for fields param. please check https://developers.facebook.com/docs/marketing-api/reference/ads-insights/ for all valid values'. Meta error type: 'OAuthException'"
    )


def test_invalid_get_account_details_error_breakdowns_list():
    breakdowns_list = ["test", "test2"]
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_account_details(
            api_endpoint="act_2573295906125403",
            level="ad",
            fields_list=["ad_id", "ad_name"],
            breakdowns_list=breakdowns_list,
        )
    assert (
        str(e.value)
        == f"Meta error. API error occurred. Error 400: Bad Request. Meta error message: '(#100) breakdowns[0] must be one of the following values: ad_format_asset, age, app_id, body_asset, call_to_action_asset, coarse_conversion_value, country, description_asset, fidelity_type, gender, hsid, image_asset, impression_device, is_conversion_id_modeled, landing_destination, link_url_asset, mdsa_landing_destination, media_asset_url, media_creator, media_destination_url, media_format, media_origin_url, media_text_content, postback_sequence_index, product_id, redownload, region, skan_campaign_id, skan_conversion_id, skan_version, title_asset, video_asset, dma, frequency_value, hourly_stats_aggregated_by_advertiser_time_zone, hourly_stats_aggregated_by_audience_time_zone, mmm, place_page_id, publisher_platform, platform_position, device_platform, standard_event_content_type, conversion_destination, marketing_messages_btn_name'. Meta error type: 'OAuthException'"
    )


def test_invalid_get_account_details_error_dates():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    with pytest.raises(MetaApiException) as e:
        meta.get_account_details(
            api_endpoint="act_2573295906125403",
            level="ad",
            fields_list=["ad_id", "ad_name"],
            breakdowns_list=["age"],
            start_date=["2021"],
            end_date=["2020"],
        )
    assert (
        str(e.value)
        == "Meta error. API error occurred. Error 400: Bad Request. Meta error message: '(#100) Must be a date representation in the format YYYY-MM-DD'. Meta error type: 'OAuthException'"
    )


def test_valid_get_account_details():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    meta.get_account_details(
        api_endpoint="act_2573295906125403",
        level="ad",
        fields_list=["ad_id", "ad_name"],
        breakdowns_list=["age"],
        start_date=["2024-04-01", "2024-04-02"],
        end_date=["2024-04-01", "2024-04-02"],
    )
    assert len(meta._all_details) == 383


def test_valid_get_campaigns_start_dates():
    logger = CustomLogger(
        logger_level=logging.DEBUG, logger_name="test"
    ).return_logger()
    meta = Meta(
        logger=logger,
        meta_url="https://graph.facebook.com/v19.0",
        api_key=meta_api_key,
    )
    meta.get_campaigns_start_dates(
        ad_account="act_2573295906125403",
        fields=[
            "id",
            "name",
            "start_time",
            "stop_time",
            "objective",
            "effective_status",
        ],
    )
    assert len(meta._all_campaign_details) == 174
