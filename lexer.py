import ply.lex as lex

tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUSPLUS', 'PLUSEQ',
    'EQUALS', 'LE', 'LT', 'GE', 'GT', 'EQEQ',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMI', 'COMMA', 'DOT'
]

reserved = {
    'for': 'FOR',
    'if': 'IF',
    'while': 'WHILE',
    'system': 'SYSTEM',
    'print': 'PRINT'
}

tokens += list(reserved.values())

t_PLUSPLUS = r'\+\+'
t_PLUSEQ   = r'\+='
t_EQEQ     = r'=='
t_EQUALS   = r'='
t_LE       = r'<='
t_GE       = r'>='
t_LT       = r'<'
t_GT       = r'>'
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_SEMI     = r';'
t_COMMA    = r','
t_DOT      = r'\.'

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    low = t.value.lower()
    if low in reserved:
        t.type = reserved[low]
        t.value = low  
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer_errors = []

def t_error(t):
    msg = f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}"
    lexer_errors.append(msg)
    t.lexer.skip(1)

def build_lexer():
    global lexer_errors
    lexer_errors = []
    return lex.lex()