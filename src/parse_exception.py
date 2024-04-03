class ParseException(Exception):
    """
    Exception raised for trying to parse tokens.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Invalid input"):
        self.message = message
        super().__init__(self.message)