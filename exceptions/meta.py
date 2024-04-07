class BaseMetaException(BaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MetaInvalidEndpointException(BaseMetaException):
    def __init__(self, message="API endpoint is required"):
        self.message = message
        super().__init__(self.message)


class MetaInvalidTokenException(BaseMetaException):
    def __init__(self, message="API key is required"):
        self.message = message
        super().__init__(self.message)