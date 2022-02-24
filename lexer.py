# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_1_Scanner
# Run: (Linux)
#   python3 lexer.py input_file_name
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
# --------------------------------------------------------
from ply import lex as lex
# from ply import yacc as yacc
import sys

# List of reserved words
words = {
    'if'    : 'KEYWORD',    'then'  : 'KEYWORD',
    'else'  : 'KEYWORD',    'map'   : 'KEYWORD',
    'to'    : 'KEYWORD',    'let'   : 'KEYWORD',
    'in'    : 'KEYWORD',    'null'  : 'NULL',
    'true'  : 'BOOL',       'false' : 'BOOL',

    'number?'   : 'PRIM', 'function?' : 'PRIM',
    'list?'     : 'PRIM', 'null?'     : 'PRIM',
    'cons?'     : 'PRIM', 'cons'      : 'PRIM',
    'first'     : 'PRIM', 'rest'      : 'PRIM',
    'arity'     : 'PRIM'
}

# Token names
tokens = [
    'INT',

    'ID',
    'KEYWORD',
    'NULL',
    'BOOL',
    'PRIM',

    'DELIMITER',
    'UNOP',
    'BINOP'
]

# Rules
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'
t_INT = r'\d+'
t_DELIMITER = '\(|\)|\[|\]|\,|\;'
t_UNOP = '\+|\-|\~'
t_BINOP = '\*|\/|\=|\!=|\<|\>|\<=|\>=|\&|\||\:='

# AlphaOther {AlphaOtherNumeric}*
def t_ID(t):
    r'[a-zA-Z_?][a-zA-Z0-9_?]*'
    # Checks for reserved words
    t.type = words.get(t.value, 'ID')
    return t

# Build lexer
lexer = lex.lex()

# Read input
data = open(sys.argv[1])

# Tokenize
with data as fp:
    for line in fp:
        try:
            lexer.input(line)
 
            for tok in lexer:
                # print(tok.type, tok.value, tok.lineno)
                print(tok)
        except EOFError:
            break

# Parser grammar rules


# build parser