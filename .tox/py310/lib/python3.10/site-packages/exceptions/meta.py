class BaseMetaException(BaseException):
    def __init__(self, message):
        self.message = f"Meta error. {message}"
        super().__init__(self.message)


class MetaInvalidEndpointException(BaseMetaException):
    def __init__(self, message="API endpoint is required"):
        self.message = message
        super().__init__(self.message)


class MetaInvalidTokenException(BaseMetaException):
    def __init__(self, message="API key is required"):
        self.message = message
        super().__init__(self.message)


class MetaApiException(BaseMetaException):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason
        self.message = f"API error occurre. Error {status_code}: {reason}"
        super().__init__(self.message)
