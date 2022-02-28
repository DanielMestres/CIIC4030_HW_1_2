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

# Sets precedence of tokens for parser
# precedence = (
#     ('left', 'UNOP'),
#     ('left', 'BINOP')
# )

# Parser grammar rules
def p_exp(p):
    #  p[0]  p[1]  p[2]  p[3]    p[4] p[5]    p[6]
    '''exp : term
            | term UNOP exp
            | term BINOP exp
            | KEYWORD exp KEYWORD exp KEYWORD exp
            | KEYWORD deflist KEYWORD exp
            | KEYWORD idlist KEYWORD exp
            | KEYWORD KEYWORD exp'''

def p_term(p):
    #  p[0]   p[1] p[2]         p[3]    p[4]
    '''term : UNOP term
            | factor
            | DELIMITER explist DELIMITER
            | factor DELIMITER DELIMITER
            | NULL
            | INT
            | BOOL'''

def p_factor(p):
    #   p[0]     p[1]    p[2]  p[3]
    '''factor : DELIMITER exp DELIMITER
                | PRIM
                | ID'''

def p_explist(p):
    #  p[0]     p[1]
    'explist : propexplist'

def p_propexplist(p):
    #    p[0]       p[1]   p[2]      p[3]
    '''propexplist : exp
                    | exp DELIMITER propexplist'''

def p_idlist(p):
    #  p[0]    p[1]
    'idlist : propidlist'

def p_propidlist(p):
    #   p[0]       p[1]   p[2]      p[3]
    '''propidlist : ID
                    | ID DELIMITER propidlist'''

def p_def(p):
    # p[0] p[1] p[2] p[3] p[4]
    'def : ID BINOP exp DELIMITER'

def p_deflist(p):
    #   p[0]    p[1]  p[2]
    '''deflist : def deflist
                | def'''

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error in input!", p)
        parser.errok()
    else:
        print("Syntax error at EOF")

# build lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Read input
data = open(sys.argv[1])
parser.parse(data.read())
