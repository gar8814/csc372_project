"""
Parser for SNFL.

The parser will take a list of tokens and parse them into statements.

e.g. ['juliet', 'is', '10'] -> ['DECLARATION juliet is 10']
"""

from parse_exception import ParseException
from declaration import Declaration

class SnflParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        '''
        Parse the tokens and return the statements.        
        '''
        statements = []
        while not self.isEOF():
            current = self.peek()

            if current.type in ['IDENTIFIER']:
                statements.append(self.declaration())
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
        if value.type not in ['NUMBER', 'STRING', 'BOOLEAN', 'CHAR']:
            raise ParseException(f"Expected value but got {value.type}")

        return Declaration(f"DECLARATION {identifier} {assign.value} {value.value}", identifier, value.value)

    def print(self):
        '''
        Parse a print statement.
        '''
        print_token = self.consume()
        if print_token.type != 'PRINT':
            raise ParseException(f"Expected 'PRINT' but got {print_token.type}")

        l_paren = self.consume()
        if l_paren.type != 'LPAREN':
            raise ParseException(f"Expected '(' but got {l_paren.type}")

        string = self.consume()
        if string.type != 'STRING' and string.type != 'IDENTIFIER':
            raise ParseException(f"Expected 'STRING' or 'IDENTIFIER' but got {string.type}")

        r_paren = self.consume()
        if r_paren.type != 'RPAREN':
            raise ParseException(f"Expected ')' but got {r_paren.type}")

        return Print(f"PRINT {l_paren.value} {string.value} {r_paren.value}", print_token.type, string.value)