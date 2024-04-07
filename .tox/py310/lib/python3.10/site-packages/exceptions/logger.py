class BaseLoggerException(BaseException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LoggerInvalidNameException(BaseLoggerException):
    def __init__(self, message="Logger name is required"):
        self.message = message
        super().__init__(self.message)


class LoggerInvalidLevelException(BaseLoggerException):
    def __init__(self, message="Logger level is required"):
        self.message = message
        super().__init__(self.message)
