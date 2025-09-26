import ply.yacc as yacc
from lexer import tokens, build_lexer

# Lista de errores sintácticos/semánticos
parse_errors = []

# Helper: limpiar errores y crear lexer antes de parsear
def parse_input(s):
    global parse_errors, parser
    parse_errors = []
    lexer = build_lexer()
    result = parser.parse(s, lexer=lexer)
    return result, parse_errors

# Reglas:
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Aceptar statements vacíos (p. ej. llaves vacías)
def p_statement(p):
    '''statement : for_statement
                 | func_call SEMI'''
    p[0] = p[1]

# For loop: init ; condition ; increment
def p_for_statement(p):
    'for_statement : FOR LPAREN assignment SEMI condition SEMI increment RPAREN LBRACE statement_list_opt RBRACE'
    init = p[3]
    cond = p[5]
    inc = p[7]
    body = p[10]

    # Comprobación semántica: misma variable en init, cond e increment
    var_init = init[1]
    var_cond = cond[1]
    var_inc = inc[1]
    semantic_msgs = []
    if not (var_init == var_cond == var_inc):
        semantic_msgs.append(f"Error semántico: la variable del for no es la misma en init/cond/inc -> init:'{var_init}', cond:'{var_cond}', inc:'{var_inc}'")
        parse_errors.extend(semantic_msgs)

    p[0] = ('for', init, cond, inc, body)

def p_statement_list_opt(p):
    '''statement_list_opt : statement_list
                          | empty'''
    p[0] = p[1] if p[1] is not None else []

# Assignment simple: ID = NUMBER  o ID = ID  (permitimos más)
def p_assignment(p):
    '''assignment : ID EQUALS expression'''
    p[0] = ('assign', p[1], p[3])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

# Condition: ID <= NUMBER  (también permitimos >=, <, >, ==)
def p_condition(p):
    '''condition : ID LE expression
                 | ID GE expression
                 | ID LT expression
                 | ID GT expression
                 | ID EQEQ expression'''
    p[0] = ('cond', p[1], p[2], p[3])

# Increment: ID ++  or ID += NUMBER
def p_increment_pp(p):
    'increment : ID PLUSPLUS'
    p[0] = ('inc', p[1], '++')

def p_increment_pluseq(p):
    'increment : ID PLUSEQ expression'
    p[0] = ('inc', p[1], '+=', p[3])

# Función: system.print("hola", i);
def p_func_call(p):
    'func_call : SYSTEM DOT PRINT LPAREN args RPAREN'
    p[0] = ('call', 'system.print', p[5])

def p_args(p):
    '''args : args COMMA arg
            | arg
            | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_arg(p):
    '''arg : STRING
           | expression'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

# Manejo de errores sintácticos
def p_error(p):
    if p:
        msg = f"Error de sintaxis en token {p.type} (valor: {p.value}) en la línea {getattr(p, 'lineno', '?')}"
    else:
        msg = "Error de sintaxis: fin de entrada inesperado"
    parse_errors.append(msg)

# Construir parser
parser = yacc.yacc()