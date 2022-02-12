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
import sys

# List of reserved words
keywords = {
    'if'    : 'IF',     'then'  : 'THEN',
    'else'  : 'ELSE',   'map'   : 'MAP',
    'to'    : 'TO',     'let'   : 'LET',
    'in'    : 'IN',     'null'  : 'NULL',
    'true'  : 'BOOL',   'false' : 'BOOL',

    'number?'   : 'PRIM', 'function?' : 'PRIM',
    'list?'     : 'PRIM', 'null?'     : 'PRIM',
    'cons?'     : 'PRIM', 'cons'      : 'PRIM',
    'first'     : 'PRIM', 'rest'      : 'PRIM',
}

# List of reserved symbols
symbols = {
    '(' : 'LPAREN',     ')' : 'RPAREN',
    '[' : 'LBRACKET',   ']' : 'RBRACKET',
    ',' : 'COMMA',      ';' : 'SEMICOLON',
    '+' : 'SIGN',       '-' : 'SIGN',
    '~' : 'UNOP',       '*' : 'BINOP',
    '/' : 'BINOP',      '=' : 'BINOP',
    '!=' : 'BINOP',     '<' : 'BINOP',
    '>' : 'BINOP',      '<=' : 'BINOP',
    '>=' : 'BINOP',     '&' : 'BINOP',
    '|' : 'BINOP',      ':=' : 'BINOP'
}

# Token names
tokens = [
    'INT',
    'ID',
    'SYMBOL',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMICOLON',
    'NULL',
    'BOOL',
    'UNOP',
    'SIGN',
    'BINOP',
    'PRIM'
]

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Regular expression rules
t_ignore  = ' \t'
t_INT = r'\d+'

def t_ID(t):
    r'[a-zA-Z_?][a-zA-Z0-9_?]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_SYMBOL(t):
    r'[^a-zA-Z0-9_?_\n][^a-zA-Z0-9_?_;_\n_\s]*'
    t.type = symbols.get(t.value, 'SYMBOL')
    if(t.type == 'SYMBOL'):
        t_error(t)
    else:
        return t

# Build lexer
lexer = lex.lex()

# Read INPUT FILE
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