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

    def __init__(self, stmt, op, left, right, dest):
        self.stmt = stmt
        self.identifier = op
        self.left = left
        self.right = right
        self.value = 0
        self.dest = dest 
        
    def __str__(self):
        return self.stmt

    def performOp(self):
        if self.identifier is 'ADD':
            self.value = self.left + self.right