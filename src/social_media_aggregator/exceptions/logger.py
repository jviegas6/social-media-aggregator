class BaseLoggerException(BaseException):
    def __init__(self, message):
        self.message = f"Logger error. {message}"
        super().__init__(self.message)


class LoggerInvalidArguments(BaseLoggerException):
    def __init__(self, message="Incorrect number of arguments provided"):
        self.message = message
        super().__init__(self.message)


# class LoggerInvalidNameException(BaseLoggerException):
#     def __init__(self, message="Logger name is required"):
#         self.message = message
#         super().__init__(self.message)


class LoggerInvalidLevelException(BaseLoggerException):
    def __init__(self, message="Logger level is required"):
        self.message = message
        super().__init__(self.message)
