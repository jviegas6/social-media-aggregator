from exceptions import *


class Meta:
    """
    Class that contains the methods to perform API calls to Meta API
    """
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def validate_init(self):
        """
        Validates the initialization of the class
        """
        if not self.api_endpoint:
            raise MetaInvalidEndpoint("API endpoint is required")
        if not self.api_key:
            raise MetaInvalidToken("API key is required")