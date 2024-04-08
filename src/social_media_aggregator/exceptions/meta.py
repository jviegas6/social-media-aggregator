class BaseMetaException(BaseException):
    def __init__(self, message):
        self.message = f"Meta error. {message}"
        super().__init__(self.message)


class MetaInvalidArguments(BaseMetaException):
    def __init__(self, message="Incorrect number of arguments provided"):
        self.message = message
        super().__init__(self.message)


# class MetaInvalidEndpointException(BaseMetaException):
#     def __init__(self, message="API endpoint is required"):
#         self.message = message
#         super().__init__(self.message)


# class MetaInvalidTokenException(BaseMetaException):
#     def __init__(self, message="API key is required"):
#         self.message = message
#         super().__init__(self.message)


class MetaApiException(BaseMetaException):
    def __init__(self, status_code, reason, response_payload=None):
        self.status_code = status_code
        self.reason = reason
        self.message = f"API error occurred. Error {status_code}: {reason}"
        if response_payload:
            self.error_message = response_payload["error"]["message"]
            self.error_type = response_payload["error"]["type"]
            complete_message = f"{self.message}. Meta error message: '{self.error_message}'. Meta error type: '{self.error_type}'"
        else:
            complete_message = self.message
        super().__init__(complete_message)
