from statement import Statement

class Declaration(Statement):
    '''
    Represents a declaration statement such as a variable or value declaration.

    Attributes:
        stmt (str): The statement.
        type (str): The type of declaration.
        identifier (Token): The identifier.
        value (Token): The value.

    Example declaration:
        x is 10

    In the above example, the identifier is 'x', and the value is '10'.
    '''

    def __init__(self, stmt, identifier, value):
        self.stmt = stmt
        self.identifier = identifier
        self.value = value

    def __str__(self):
        return self.stmt

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.stmt == other.stmt and self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.stmt) ^ hash(self.type) ^ hash(self.value)

    def __copy__(self):
        return Declaration(self.stmt, self.value)