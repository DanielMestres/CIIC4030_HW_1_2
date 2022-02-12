# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_1_Scanner
# To run: python3 lexer.py "input file name"
# --------------------------------------------------------
from ply import lex as lex
from ply.lex import TOKEN
import sys

# List of reserved words
keywords = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'map' : 'MAP',
    'to' : 'TO',
    'let' : 'LET',
    'in' : 'IN',
    'null' : 'NULL',
    'true' : 'TRUE',
    'false' : 'FALSE'
}

# Token names
tokens = [
    'ID',
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
] + list(keywords.values()) # Adds reserved words

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore  = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value,'ID')    # Check for reserved words
    return t

# Regular expression rules for other tokens
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# End-of-File handling rule
# def t_eof(t):
#     # Get more input (Example)
#     more = input('... ')
#     if more:
#         self.lexer.input(more)
#         return self.lexer.token()
#     return None

# Build lexer
lexer = lex.lex()

# reading INPUT FILE
data = open(sys.argv[1])

# Tokenize
with data as fp:
    for line in fp:
        try:
            lexer.input(line)
 
            for tok in lexer:
                # print(tok.type, tok.value, tok.lineno) ?
                print(tok)
 
        except EOFError:
            break