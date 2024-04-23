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

class IfStatement(Statement):
    def __init__(self, condition, then_branch, else_branch=None):
        super().__init__("IF_STATEMENT")
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(Statement):
    def __init__(self, condition, body):
        super().__init__("WHILE_STATEMENT")
        self.condition = condition
        self.body = body
