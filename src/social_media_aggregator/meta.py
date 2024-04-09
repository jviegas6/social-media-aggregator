from .exceptions.meta import (
    MetaApiException,
    MetaInvalidArguments,
)
from .helpers.helpers import validate_arguments
from .logger import CustomLogger
from logging import Logger
import requests
import json
import time


class Meta:
    """
    Class that contains the methods to perform API calls to Meta API
    """

    @validate_arguments(
        (Logger, True), (str, True), (str, True), exception_class=MetaInvalidArguments
    )
    def __init__(self, logger: Logger, meta_url: str, api_key: str):
        self.meta_url = meta_url
        self.api_key = api_key
        self.logger = logger

    @staticmethod
    def _get_meta_data(
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
            temp_result_list = Meta._get_meta_data(logger, [], request_url)
            result_list.extend(temp_result_list)

        else:
            logger.info(f"Data retrieval was succesfull")
            result_list.extend(response_text["data"])
            if "paging" in response_text.keys():
                if "next" in response_text["paging"].keys():
                    logger.info(f"Response has a next page")
                    next_url = response_text["paging"]["next"]
                    temp_result_list = Meta._get_meta_data(
                        logger, result_list, next_url
                    )
                    result_list.extend(temp_result_list)

            else:
                logger.info(f"This was the last page of the response")

        return result_list

    @validate_arguments((str, True), exception_class=MetaInvalidArguments)
    def get_accounts(self, api_endpoint: str = "me/adaccounts"):
        """
        Method to read ad accounts from Meta API

        Args:
            api_endpoint (str, optional): The Meta endpoint for adaccounts. Defaults to "me/adaccounts".
        """
        # self._validate_arguments()
        self.logger.info(f"Getting ad accounts from Meta API")
        meta_complete_url = (
            f"{self.meta_url}/{api_endpoint}?access_token={self.api_key}"
        )
        self.logger.info(f"Meta complete URL: {meta_complete_url}")

        all_accounts = Meta._get_meta_data(self.logger, [], meta_complete_url)

        self.logger.debug(f"Accounts retrieved: {all_accounts}")

        self._all_accounts = all_accounts
        return all_accounts

    @validate_arguments(
        (str, True),
        (list, False),
        (list, False),
        (str, False),
        (list, False),
        (list, False),
        exception_class=MetaInvalidArguments,
    )
    def get_account_details(
        self,
        api_endpoint: str,
        fields_list: list = None,
        breakdowns_list: list = None,
        level: str = None,
        start_date: list = None,
        end_date: list = None,
    ):
        """
        Method to get the details of an account from Meta API

        Args:
            api_endpoint (str): _description_
            fields_list (list, optional): _description_. Defaults to None.
            breakdowns_list (list, optional): _description_. Defaults to None.
            level (str, optional): _description_. Defaults to None.
            start_date (str, optional): _description_. Defaults to None.
            end_date (str, optional): _description_. Defaults to None.
        """
        self.logger.info(f"Getting account details from Meta API")

        meta_sub_part_url = []
        if level:
            meta_sub_part_url.append(f"level={level}")
        if fields_list:
            meta_sub_part_url.append(f"fields={','.join(fields_list)}")
        if breakdowns_list:
            meta_sub_part_url.append(f"breakdowns={','.join(breakdowns_list)}")
        if start_date and end_date:
            for i, part_date in enumerate(start_date):
                if i == 0:
                    date_string = (
                        "{'since':'" + part_date + "','until':'" + end_date[i] + "'}"
                    )
                else:
                    date_string += (
                        ",{'since':'" + part_date + "','until':'" + end_date[i] + "'}"
                    )

            meta_sub_part_url.append(f"time_ranges=[{date_string}]")

        if self.api_key:
            meta_sub_part_url.append(f"access_token={self.api_key}")

        if len(meta_sub_part_url) > 0:
            meta_complete_url = (
                f"{self.meta_url}/{api_endpoint}/insights?{'&'.join(meta_sub_part_url)}"
            )
        else:
            meta_complete_url = f"{self.meta_url}/{api_endpoint}/insights"

        self.logger.debug(f"Meta complete URL: {meta_complete_url}")

        all_details = Meta._get_meta_data(self.logger, [], meta_complete_url)

        self.logger.debug(f"Lenght of details: {len(all_details)}")

        self._all_details = all_details
        return all_details
