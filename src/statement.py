class Statement:

    stmt = None
    type = None

    def __init__(self, stmt, type=None):
        self.stmt = stmt
        self.type = type

    def __str__(self):
        return self.stmt

    def __repr__(self):
        return self.__str__()