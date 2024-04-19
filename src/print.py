from statement import Statement

class Print(Statement):
    '''
    Represents a print statement.
    '''
    def __init__(self, stmt, type, value):
        self.stmt = stmt
        self.type = type
        self.value = value

    def __repr__(self):
        return f'PRINT {self.value}'

    def __str__(self):
        return f'PRINT {self.value}'