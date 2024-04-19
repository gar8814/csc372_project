class TypeError(Exception):
    """
    Exception raised for trying to do operations on incorrect types.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Type Missmatch!"):
        self.message = message
        super().__init__(self.message)