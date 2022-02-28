# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_1_Scanner
# Run: (Linux)
#   python3 file_name.py input_file_name
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
# --------------------------------------------------------
from ply import lex as lex
from ply import yacc as yacc
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

# Token map
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

with data as fp:
    for line in fp:
        try:
            lexer.input(line)
        except EOFError:
            break

# Sets precedence of tokens for parser
precedence = (
    ('left', 'UNOP'),
    ('left', 'BINOP')
)

# Parser grammar rules
def p_exp(p):
    #  p[0]  p[1]  p[2]  p[3]    p[4] p[5]    p[6]
    '''exp : term UNOP exp
            | term BINOP exp
            | KEYWORD exp KEYWORD exp KEYWORD exp
            | KEYWORD def KEYWORD exp
            | KEYWORD idlist KEYWORD exp'''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

    # TODO Implement rules for term BINOP exp
    #

    if p[1] == 'if' & p[3] == 'then' & p[5] == 'else':
        if p[2]:
            p[0] = p[4]
        else:
            p[0] = p[6]

    # TODO Implement rules for KEYWORD def KEYWORD exp
    # if p[1] == 'let' & p[3] == 'in':

    # TODO Implement rules for KEYWORD idlist KEYWORD exp
    # if p[1] == 'map' & p[3] == 'to':


def p_term(p):
    #  p[0]   p[1] p[2]         p[3]    p[4]
    '''term : UNOP term
            | factor DELIMITER explist DELIMITER
            | NULL
            | INT
            | BOOL'''

    # TODO Implement rules for UNOP term
    #

    # TODO Implement rules for factor DELIMITER explist DELIMITER
    #

    if p[1] == 'null':
        p[0] = None

    if isinstance(p[1], (int, bool)):
        p[0] = p[1]

def p_factor(p):
    #   p[0]     p[1]    p[2]  p[3]
    '''factor : DELIMITER exp DELIMITER
                | PRIM
                | ID'''

    # TODO Implement rules for DELIMITER exp DELIMITER
    #

    # TODO Implement rules for PRIM
    #

    # TODO Implement rules for ID
    #

def p_explist(p):
    #  p[0]     p[1]
    'explist : DELIMITER propexplist DELIMITER'

    # TODO Implement rules for propexplist
    #

def p_propexplist(p):
    #    p[0]       p[1]   p[2]      p[3]
    '''propexplist : exp
                    | exp DELIMITER propexplist'''

    # TODO Implement rules for exp
    #

    # TODO Implement rules for exp DELIMITER propexplist
    #

def p_idlist(p):
    #  p[0]    p[1]
    'idlist : DELIMITER propidlist DELIMITER'

    # TODO Implement rules for DELIMITER propidlist DELIMITER
    #

def p_propidlist(p):
    #   p[0]       p[1]   p[2]      p[3]
    '''propidlist : ID
                    | ID DELIMITER propidlist'''

    # TODO Implement rules for ID
    #

    # TODO Implement rules for ID DELIMITER propidlist
    #

def p_def(p):
    # p[0] p[1] p[2] p[3] p[4]
    'def : ID BINOP exp DELIMITER'

    if p[2] == ':=' & p[4] == ';':
        p[1] = p[3]
        p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# build parser
parser = yacc.yacc()

with data as fp:
    for line in fp:
        try:
            parser.parse(line)
        except EOFError:
            break
