"""
Parser for SNFL.

The parser will take a list of tokens and parse them into statements.

e.g. ['juliet', 'is', '10'] -> ['DECLARATION juliet is 10']
"""

from parse_exception import ParseException
from declaration import Declaration
from operations import Operations

class SnflParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        '''
        Parse the tokens and return the statements.        
        '''
        print("In SnflParser.parse()")
        statements = []
        while not self.isEOF():
            current = self.peek()
            print(f"current: {current}")
            if current.type in ['IDENTIFIER']:
                statements.append(self.declaration())
                print(statements)
            else:
                raise ParseException(f"Unexpected token: {current.type}")
            
        return statements

    def peek(self):
        '''
        Peek at the current token.
        '''
        return self.tokens[self.current]

    def consume(self):
        '''
        Consume the current token and return the statement.
        ''' 
        token = self.tokens[self.current]
        self.current += 1
        return token

    def isEOF(self):
        return self.current >= len(self.tokens)
    
    def add(self):
        '''
        parse an operation
        '''
        token = self.consume()
        if token.type == 'ADD':
            return self.parse_add(token)
        else:
            raise ParseException(f"Invalid declaration: {token}")


    def declaration(self):
        '''
        Parse a declaration.
        '''
        token = self.consume()
        if token.type == 'IDENTIFIER':
            return self.parse_declaration(token)
        else:
            raise ParseException(f"Invalid declaration: {token}")
    
    def parse_declaration(self, declaration):
        '''
        Parse a declaration.
        '''
        identifier = declaration.value

        assign = self.consume()
        if assign.type != 'ASSIGN':
            raise ParseException(f"Expected assign but got {assign.type}")

        value = self.consume()
        if value.type in ['NUMBER', 'STRING', 'BOOLEAN', 'CHAR']:
            return Declaration(f"DECLARATION {identifier} {assign.value} {value.value}", identifier, value.value)
        elif value.type in ['ADD', 'SUB', 'DIV', 'MULT', 'MOD', 'AND',  'OR', 'GT', 'LT', 'GTE', 'LTE', 'EQ']:
            print(f"value.type = {value.type}, value.value={value.value}")
            openParenth = self.consume()
            print(openParenth.value)
            firstVal = self.consume()
            print(firstVal.value)
            comma = self.consume() 
            print(comma.value)
            secondVal = self.consume()
            print(secondVal.value)
            self.consume()
            return Operations(f"ADD {identifier} {assign.value} {firstVal.value} + {secondVal.value}", value.value, firstVal.value, secondVal.value)
        else:
            raise ParseException(f"Expected value but got {value.type}")

        return Declaration(f"DECLARATION {identifier} {assign.value} {value.value}", identifier, value.value)
    
    def parse_add(self, addOp):
        operation = addOp.value
        add_op = self.consume()
        if add_op != 'ADD':
            raise ParseException(f"Expected add but got {add_op.type}")
        
        

