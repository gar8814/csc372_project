"""
Parser for SNFL.

The parser will take a list of tokens and parse them into statements.

e.g. ['juliet', 'is', '10'] -> ['DECLARATION juliet is 10']
"""

from parse_exception import ParseException
from declaration import Declaration
from print import Print
from operations import Operations
from statement import IfStatement, WhileStatement


class SnflParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        # Add additional funcs to self.funcs 
        self.__funcs = {
            'IDENTIFIER': self.__declaration,
            'ADD': self.__op,
            'SUB': self.__op,
            'DIV': self.__op,
            'MULT': self.__op,
            'MOD': self.__op,
            'AND': self.__op,
            'OR': self.__op,
            'GT': self.__op,
            'LT': self.__op,
            'GTE': self.__op,
            'LTE': self.__op,
            'EQ': self.__op,
            'PRINT': self.__print,
            'IDENTIFIER': self.__declaration,
            'ADD': self.__op,
            'PRINT': self.__print,
            'IF': self.parse_if_statement,
            'WHILE': self.parse_while_statement
        }

    def parse(self):
        '''
        Parse the tokens and return the statements.        
        '''
        statements = []
        while not self.__isEOF():
            current = self.__peek()
            # print(f"current: {current.type}")
            # determine which function to call to handle the incoming statement. 
            func = self.__funcs.get(current.type)
            statements.append(func())
            
        return statements


    def __peek(self):
        '''
        Peek at the current token.
        '''
        return self.tokens[self.current]

    def __consume(self):
        '''
        Consume the current token and return the statement.
        ''' 
        token = self.tokens[self.current]
        self.current += 1
        return token

    def __isEOF(self):
        return self.current >= len(self.tokens)
    
    # ------------------------------------------------------------------------------------------------------------------
    # This is where you want to create more handlers for additional statement types to parse 
    # this ultimatly needs to return an object that describes the statement and this object class should 
    # at least inherit from Statement
    # ------------------------------------------------------------------------------------------------------------------

    def parse_if_statement(self):
        '''
        Parsing the if-else statements
        '''
        self.expect('IF')  # Consume the 'IF' token
        self.expect('LPAREN')  # Consume the '(' token

        condition = self.parse_expression()

        self.expect('RPAREN')  # Consume the ')' token
        self.expect('LBRACE')  # Consume the '{' token

        then_branch = self.parse_block()

        else_branch = None
        next = self.__consume()
        if (self.__isEOF()):
            return IfStatement(condition, then_branch, else_branch)
        
        next = self.__peek()
        if next.type == 'ELSE':
            self.expect('ELSE')  # Consume the 'ELSE' token
            self.expect('LBRACE')
            else_branch = self.parse_block()
            self.expect('RBRACE')

        return IfStatement(f"if({condition} then {then_branch} else {else_branch}",condition, then_branch, else_branch)



    # Method to parse while statements
    def parse_while_statement(self):
        '''
        Parsing the while loops
        '''
        self.expect('WHILE')
        self.expect('LPAREN')

        condition = self.parse_expression()

        self.expect('RPAREN')
        self.expect('LBRACE')

        body = self.parse_block()
        
        self.expect('RBRACE')

        return WhileStatement(condition, body)

    def expect(self, expected_type):
        """
        Ensure the next token is of the expected type and consume it.
        """
        token = self.__peek()
        if token.type != expected_type:
            raise ParseException(f"Expected token type {expected_type} but got {token.type}")
        return self.__consume()

    def parse_expression(self):
        """
        Parse an expression and return an appropriate expression object.
        """
        # token = self.__peek()
        token = self.__consume()
        if token.type in ['NUMBER', 'STRING', 'BOOLEAN', 'CHAR', 'IDENTIFIER']:
            # Simple literals or variable names
            # self.__consume()
            return token
        elif token.type in ['ADD', 'SUB', 'DIV', 'MULT', 'MOD', 'AND', 'OR', 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NOT']:
            # Operator-based expressions
            return self.__parse_op(token)
        else:
            raise ParseException(f"Unexpected token type in expression: {token.type}")

    def parse_block(self):
        """
        Parse a block of statements until the end of the block.
        """
        statements = []
        current = self.__peek()
        while current.value != '}':
            statements.append(self.parse_statement())
            current = self.__peek()
        return statements

    def check(self, token_type):
        """
        Check if the next token is of the given type without consuming it.
        """
        next = self.__peek()
        return next.type == token_type

    def parse_statement(self):
        """
        Parse a single statement.
        """
        # token = self.__consume()
        token = self.__peek()
        if token.type in self.__funcs:
            return self.__funcs[token.type]()
        else:
            raise ParseException(f"Unrecognized token type for statement: {token.type}")
    
    def __op(self):
        '''
        parse an operation
        '''
        token = self.__consume()
        return self.__parse_op(token)

    def __declaration(self):
        '''
        Parse a declaration.
        '''
        token = self.__consume()
        if token.type == 'IDENTIFIER':
            return self.__parse_declaration(token)
        else:
            raise ParseException(f"Invalid declaration: {token}")
    
    def __parse_declaration(self, declaration):
        '''
        Parse a declaration.
        '''
        identifier = declaration.value

        assign = self.__consume()
        if assign.type != 'ASSIGN':
            raise ParseException(f"Expected assign but got {assign.type}")

        value = self.__consume()
        if value.type in ['NUMBER', 'STRING', 'BOOLEAN', 'CHAR']:
            return Declaration(f"DECLARATION {identifier} {assign.value} {value.value}", identifier, value.value)
        elif value.type in ['ADD', 'SUB', 'DIV', 'MULT', 'MOD', 'AND',  'OR', 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NOT']:
            return self.__parse_op(value, identifier)
        else:
            raise ParseException(f"Expected value but got {value.type}")
    
    def __parse_op(self, addOp, dest=None ):
        '''
        Parse an operation statement
        '''
        operation = addOp.value
        # print(operation)
        next = self.__consume()

        leftSide = self.__consume()
        # What if this is another operation statement

        if operation == 'not':
            self.__consume()
            return Operations(f"{operation}({leftSide.value})", operation,leftSide.value,None, dest)
            
        if leftSide in self.__funcs.keys():
            pass
        next = self.__consume()

        # What if this is another operation statement
        rightSide = self.__consume()
        if rightSide in self.__funcs.keys():
            pass
        next = self.__consume()
        return Operations(f"{operation}({leftSide.value},{rightSide.value})", operation,leftSide.value,rightSide.value, dest)

    def __print(self):
        '''
        Parse a print statement.
        '''
        token = self.__consume()
        if token.type != 'PRINT':
            raise ParseException(f"Invalid print statement: {token}")
        
        l_paren = self.__consume()
        if l_paren.type != 'LPAREN':
            raise ParseException(f"Expected '(' but got {l_paren}")
        
        string = self.__consume()
        if string.type != 'STRING' and string.type != 'IDENTIFIER' and string.type != 'NUMBER' and string.type != 'BOOLEAN' and string.type != 'CHAR':
            raise ParseException(f"Cannot print - received {string.type}")
        
        r_paren = self.__consume()
        if r_paren.type != 'RPAREN':
            raise ParseException(f"Expected ')' but got {r_paren}")
        
        return Print(f"PRINT {l_paren.value} {string.value} {r_paren.value}", token.type, string.value)
