"""
This module defines the SnflTokenizer class, which is used for tokenizing input data.

An example of tokenization is breaking down the input data into individual tokens.

e.g. "juliet is 10" -> ['juliet', 'is', '10']
"""

import ply.lex as lex

class SnflTokenizer:

    def __init__(self):
        self.lexer = None

    tokens = (

        'IDENTIFIER', 'ASSIGN', 'EQUAL', 'NUMBER', 'STRING', 'BOOLEAN', 'CHAR', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
        'ADD', 'SUB', 'DIV', 'MULT', 'MOD', 'AND', 'OR', 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'COMMA', 'PRINT', 'NOT', 'IF', 'ELSE', 'WHILE'

    )

    t_ASSIGN = r'is'
    t_EQUAL = r'='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
    t_IDENTIFIER = r'(?!(is)\b)(?!(add)\b)(?!(sub)\b)(?!(div)\b)(?!(mult)\b)(?!(mod)\b)(?!(and)\b)(?!(or)\b)(?!(gt)\b)(?!(lt)\b)(?!(gte)\b)(?!(lte)\b)(?!(eq)\b)(?!(not)\b)[a-zA-Z_][a-zA-Z_0-9]*'
    t_ignore_COMMENT = r'//.*'

    t_ADD = r'add'
    t_SUB = r'sub'
    t_DIV = r'div'
    t_MULT = r'mult'
    t_MOD = r'mod'
    t_AND = r'and'
    t_OR = r'or'
    t_NOT = r'not'
    t_GT = r'gt'
    t_LT = r'lt'
    t_GTE = r'gte'
    t_LTE = r'lte'
    t_EQ = r'eq'
    t_COMMA = r','

    def t_NUMBER(self, t):
        r'[+-]?\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\".*?\"'
        t.value = t.value[1:-1]  # remove the double quotes
        return t

    def t_BOOLEAN(self, t):
        r'True|False'
        t.value = (lambda x: True if x == 'True' else False)(t.value)
        return t

    def t_CHAR(self, t):
        r"'.'"
        t.value = t.value[1:-1]  # remove the single quotes
        return t

    def t_PRINT(self, t):
        r'print'
        return t

    def t_IF(self, t):
        r'if'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_WHILE(self, t):
        r'while'
        return t
    
    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenize(self, data):
        self.lexer.input(data)
        return [tok for tok in self.lexer]
