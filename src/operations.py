from declaration import Declaration

class Operations(Declaration):
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

    def __init__(self, stmt, op, left, right):
        self.stmt = stmt
        self.identifier = op
        self.left = left
        self.right = right
        self.value = 0 
        

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
        return Operations(self.stmt, self.value)
    
    def performOp(self):
        if self.identifier is 'ADD':
            self.value = self.left + self.right