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

            for token in lexer:
                print(token)
        except EOFError:
            break

###############################_FIX_###################################

# Sets precedence of tokens for parser
precedence = (
    ('left', 'UNOP'),
    ('left', 'BINOP')
)

# Parser grammar rules

# Expressions
def p_exp_binop(p):
    'exp : term BINOP exp'
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_exp_unop(p):
    'exp : term UNOP exp'
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_exp_if(p):
    'exp : KEYWORD exp KEYWORD exp KEYWORD exp'
    if p[1] == 'if' & p[3] == 'then' & p[5] == 'else':
        if p[2] == true:
            p[0] = p[4]
        else:
            p[0] = p[6]
    else:
        p_error(p)

def p_exp_let(p):
    'exp : KEYWORD def KEYWORD exp'

def p_exp_map(p):
    'exp : KEYWORD idlist KEYWORD exp'


# Terms
def p_term_unop(p):
    'term : UNOP term'

def p_term_fact(p):
    'term : factor DELIMITER explist DELIMITER'

def p_term_null(p):
    'term : NULL'

def p_term_int(p):
    'term : INT'

def p_term_bool(p):
    'term : BOOL'


# Factors
def p_factor_exp(p):
    'factor : DELIMITER exp DELIMITER'

def p_factor_prim(p):
    'factor : PRIM'

def p_factor_id(p):
    'factor : ID'


def p_explist(p):
    'explist : propexplist'

# PropExpLists
def p_propexplist_exp(p):
    'propexplist : exp'

def p_propexplist_self(p):
    'propexplist : exp DELIMITER propexplist'


def p_idlist(p):
    'idlist : propidlist'

# PropIdLists
def p_propidlist_list(p):
    'propidlist : ID'

def p_propidlist_self(p):
    'propidlist : ID DELIMITER propidlist'


def p_def(p):
    'def : ID BINOP exp'
    if p[2] == ':=':
       p[0] = p[1] = p[3]

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
