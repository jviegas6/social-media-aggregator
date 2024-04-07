from src.exceptions.meta import (
    MetaInvalidEndpointException,
    MetaInvalidTokenException,
    MetaApiException,
)
from src.regus_social_media.logger import CustomLogger
from logging import Logger
import requests
import json
import time


class Meta:
    """
    Class that contains the methods to perform API calls to Meta API
    """

    def __init__(self, logger: Logger, meta_url: str, api_key: str):
        self.meta_url = meta_url
        self.api_key = api_key
        self.logger = logger

    def _validate_arguments(self):
        """
        Validates the initialization of the class
        this test validates if any of the arguments is missing or is an empty string
        """
        if not self.meta_url:
            self.logger.error("Meta URL is required")
            raise MetaInvalidEndpointException()
        if not self.api_key:
            self.logger.error("Meta URL is required")
            raise MetaInvalidTokenException()

    @staticmethod
    def get_meta_data(
        logger: Logger, result_list: list, meta_complete_url: str = None
    ) -> list:
        """
        Recursive method to get all the data from Meta API
        Because the Meta API has a limit of n results per page, this method will call itself until there are no more results to get

        Args:
            logger (Logger): Logger object
            results_list (list): List to store the results
            meta_complete_url (str, optional): Meta URL. Defaults to None.

        Returns:
            list: List with all the results from Meta API
        """
        request_url = meta_complete_url

        response = requests.get(request_url)
        response_text = json.loads(response.text)

        if response.status_code != 200 and response.status_code != 429:
            logger.error(
                f"An error has occured. Error {response.status_code}: {response.reason}"
            )
            logger.error(f"Response: {response_text}")
            raise MetaApiException(response.status_code, response.reason, response_text)

        elif response.status_code == 429:  # pragma: no cover
            logger.info(f"Rate limit exceeded. Waiting 1 minute")
            time.sleep(60)
            logger.info(f"Retrying request")
            temp_result_list = Meta.get_meta_data(logger, result_list, request_url)
            result_list.extend(temp_result_list)

        else:
            logger.info(f"Data retrieval was succesfull")
            result_list.extend(response_text["data"])

            if "next" in response_text["paging"].keys():
                logger.info(f"Response has a next page")
                next_url = response_text["paging"]["next"]
                temp_result_list = Meta.get_meta_data(logger, result_list, next_url)
                result_list.extend(temp_result_list)

            else:
                logger.info(f"This was the last page of the response")

        return result_list

    def get_accounts(self, api_endpoint: str = "me/adaccounts"):
        """
        Method to read ad accounts from Meta API

        Args:
            api_endpoint (str, optional): The Meta endpoint for adaccounts. Defaults to "me/adaccounts".
        """
        self._validate_arguments()
        self.logger.info(f"Getting ad accounts from Meta API")
        meta_complete_url = (
            f"{self.meta_url}/{api_endpoint}?access_token={self.api_key}"
        )
        self.logger.info(f"Meta complete URL: {meta_complete_url}")

        all_accounts = Meta.get_meta_data(self.logger, [], meta_complete_url)

        self.logger.debug(f"Accounts retrieved: {all_accounts}")

        self._all_accounts = all_accounts
