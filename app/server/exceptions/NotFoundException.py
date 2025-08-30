from app.server.exceptions.MeteoException import MeteoException


class NotFoundException(MeteoException):
    """Exception raised for not found elements

    Attributes:
        message -- explanation of the error
        code -- error code
    """

    def __init__(self, message="Element not found", code=404):
        super().__init__(message, code)

