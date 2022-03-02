# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_1_&_2_Scanner_&_Parser
# Run: (Linux)
#   python3 parser.py input_file_name
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
# --------------------------------------------------------
from ply import lex as lex
from ply import yacc as yacc
import sys
import logging

##########################_Scanner_#############################

# Reserved words map ('word' : 'TOKEN')
words = {
    'if'    : 'IF',    'then'  : 'THEN',
    'else'  : 'ELSE',  'map'   : 'MAP',
    'to'    : 'TO',    'let'   : 'LET',
    'in'    : 'IN',    'null'  : 'NULL',

    'true'  : 'BOOL',  'false' : 'BOOL',

    'number?'   : 'PRIM', 'function?' : 'PRIM',
    'list?'     : 'PRIM', 'null?'     : 'PRIM',
    'cons?'     : 'PRIM', 'cons'      : 'PRIM',
    'first'     : 'PRIM', 'rest'      : 'PRIM',
    'arity'     : 'PRIM'
}

# Token list
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

    'DELIMITER',
    'PLUS',
    'MINUS',
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
t_DELIMITER = r'\(|\)|\[|\]|\,|\;'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_BINOP = r'\~|\*|\/|\=|\!=|\<|\>|\<=|\>=|\&|\||\:='

# AlphaOther {AlphaOtherNumeric}*
def t_ID(t):
    r'[a-zA-Z_?][a-zA-Z0-9_?]*'
    # Checks for reserved words
    t.type = words.get(t.value, 'ID')
    return t

##########################_Parser_##############################

# Parser grammar rules
def p_exp(p):
    #  p[0]  p[1] p[2] p[3] p[4] p[5] p[6]
    '''exp : term
           | term PLUS exp
           | term MINUS exp
           | term BINOP exp
           | IF exp THEN exp ELSE exp
           | LET defplus IN exp
           | IN exp
           | MAP idlist TO exp
           | MAP TO exp
    '''
    pass

def p_term(p):
    #  p[0]   p[1]   p[2]      p[3]    p[4]
    '''term : factor
            | BINOP term
            | MINUS term
            | factor DELIMITER explist DELIMITER
            | NULL
            | INT
            | BOOL
    '''

def p_factor(p):
    #  p[0]     p[1]     p[2]  p[3]
    '''factor : DELIMITER exp DELIMITER
              | PRIM
              | ID
    '''
    pass

def p_explist(p):
    #   p[0]      p[1]
    '''explist : propexplist
    '''
    pass

def p_propexplist(p):
    #   p[0]        p[1]  p[2]      p[3]
    '''propexplist : exp
                   | exp DELIMITER propexplist
    '''
    pass

def p_idlist(p):
    #  p[0]      p[1]
    '''idlist : propidlist
    '''

def p_propidlist(p):
    #   p[0]       p[1]  p[2]     p[3]
    '''propidlist : ID
                  | ID DELIMITER propidlist
    '''
    pass

def p_defplus(p):
    #   p[0]    p[1]  p[2]
    '''defplus : def
               | def defplus
    '''
    pass

def p_def(p):
    #  p[0] p[1] p[2] p[3] p[4]
    '''def : ID BINOP exp DELIMITER
    '''
    pass

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error in input!", p, "line:", p.lexer.lineno)
        parser.errok()

##########################_Debug_&_Running_#############################

# Set up a logging object
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Build scanner and parser
lexer = lex.lex()
parser = yacc.yacc(debug=True, debuglog=log)

# Read input
data = open(sys.argv[1])

# Parse input
parser.parse(data.read())
