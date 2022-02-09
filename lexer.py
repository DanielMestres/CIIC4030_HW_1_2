from .ply import lex as lex

tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
)



# Build lexer
lexer = lex.lex()
