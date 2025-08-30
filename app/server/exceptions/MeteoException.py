class MeteoException(Exception):
    """Exception raised for nft errors

    Attributes:
        message -- explanation of the error
        code -- error code
    """

    def __init__(self, message="Generic error", code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

    def to_json(self):
        return {'message': self.message}
