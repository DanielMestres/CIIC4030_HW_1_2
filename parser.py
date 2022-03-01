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
    'if'    : 'IF',    'then'  : 'THEN',
    'else'  : 'ELSE',    'map'   : 'MAP',
    'to'    : 'TO',    'let'   : 'LET',
    'in'    : 'IN',    'null'  : 'NULL',
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
    'IF',
    'THEN',
    'ELSE',
    'MAP',
    'TO',
    'LET',
    'IN',
    'NULL',
    'BOOL',
    'PRIM',

    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMICOLON',

    'PLUS',
    'MINUS',
    'TILDE',

    'TIMES',
    'DIVIDE',
    'POWER',
    'EQUAL',
    'NEQUAL',
    'LESS',
    'MORE',
    'LESSEQ',
    'MOREEQ',
    'AND',
    'OR',
    'ASSIGN'
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
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TILDE = r'\~'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'\^'
t_EQUAL = r'\='
t_NEQUAL = r'\!='
t_LESS = r'\<'
t_MORE = r'\>'
t_LESSEQ = r'\<='
t_MOREEQ = r'\>='
t_AND = r'\&'
t_OR = r'\|'
t_ASSIGN = r'\:='

# AlphaOther {AlphaOtherNumeric}*
def t_ID(t):
    r'[a-zA-Z_?][a-zA-Z0-9_?]*'
    # Checks for reserved words
    t.type = words.get(t.value, 'ID')
    return t

# Sets precedence of tokens for parser
precedence = (
     ('nonassoc', 'LESS', 'MORE'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
     ('left', 'POWER'),
     ('right', 'UMINUS')
)

# Parser grammar rules
def p_exp(p):
    '''exp : term
            | term PLUS exp
            | term MINUS exp
            | term TIMES exp
            | term DIVIDE exp
            | term POWER exp
            | term EQUAL exp
            | term NEQUAL exp
            | term LESS exp
            | term MORE exp
            | term LESSEQ exp
            | term MOREEQ exp
            | term AND exp
            | term OR exp
            | term ASSIGN exp

            | IF exp THEN exp ELSE exp
            | LET defplus IN exp
            | MAP idlist TO exp
            | MAP TO exp'''
    pass

def p_term(p):
    '''term : MINUS term %prec UMINUS
            | TILDE term %prec UMINUS
            | PLUS term
            | TIMES term
            | DIVIDE term
            | EQUAL term
            | NEQUAL term
            | LESS term
            | MORE term
            | LESSEQ term
            | MOREEQ term
            | AND term
            | OR term

            | factor LPAREN explist RPAREN
            | NULL
            | INT
            | BOOL'''

def p_factor(p):
    '''factor : LPAREN exp RPAREN
                | PRIM
                | ID'''
    pass

def p_explist(p):
    'explist : propexplist'
    pass

def p_propexplist(p):
    '''propexplist : exp
                    | exp COMMA propexplist'''
    pass

def p_idlist(p):
    'idlist : propidlist'

def p_propidlist(p):
    '''propidlist : ID
                    | ID COMMA propidlist'''
    pass

def p_defplus(p):
    '''defplus : def defplus
                | def'''

def p_def(p):
    'def : ID ASSIGN exp SEMICOLON'
    pass

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error in input!", p, "line:", p.lexer.lineno)
        parser.errok()
    else:
        print("Syntax error at EOF")

# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# read input and build parser and lexer
data = open(sys.argv[1])
lexer = lex.lex()
parser = yacc.yacc(debug=True, debuglog=log)
lexer.input(data)

while True:
    try:
        s = input(data)
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s, debug=True)
    print(result)
