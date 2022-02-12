# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_1_Scanner
# Run:
#   python3 lexer.py "input file name"
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
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

# Token names TODO: 
tokens = [
    'LOWER',
    'UPPER',
    'OTHER',
    'DIGIT',
    'ALPHA',
    'ALPHAOTHER',
    'ALPHAOTHERNUMERIC',
    'DELIMITER',
    'OPERATOR',
    'INT'
] + list(keywords.values()) # Adds keywords

# Regular expression rules
t_ignore  = ' \t'
t_LOWER = r'([a-z])'
t_UPPER = r'([A-Z])'
t_OTHER = r'\?' # TODO: Add other characters
t_DIGIT = r'([0-9])'
t_ALPHA = r'(' + t_UPPER + r'|' + t_LOWER + r')'
t_ALPHAOTHER = r'(' + t_ALPHA + r'|' + t_OTHER + r')'
t_ALPHAOTHERNUMERIC = r'(' + t_ALPHAOTHER + r'|' + t_DIGIT + r')'
t_DELIMITER = r'(' + r'\(' + r'|' + r'\)' + r'|' + r'\[' + r'|' + r'\]' + r'|' + r'\,' + r'|' + r'\;' + r')'

def t_OPERATOR(t):
    # TODO: Distinguish double characters, such as "<=" and "<"
    r'\<'
    return t

@TOKEN(t_DIGIT)
def t_INT(t):
    # TODO: Implement Digit+
    r'(' + t_DIGIT + r'*' + r')' 
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