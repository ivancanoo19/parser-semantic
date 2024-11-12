import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'KEYWORD',
    'IDENTIFIER',
    'LITERAL',
    'REVALUAR',
    'PARIZQ', 'PARDER', 'CORIZQ', 'CORDER',
    'MAS', 'MENOS', 'POR', 'DIVIDIDO',
    'ENTERO', 'DECIMAL', 'PTCOMA'
]

# Definiciones de patrones de tokens
t_REVALUAR = r'Evaluar\b'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PTCOMA = r';'
t_ENTERO = r'\d+'
t_DECIMAL = r'\d+\.\d+'
t_ignore = ' \t'  # Ignora espacios y tabulaciones

# Saltos de línea
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Precedencia de operadores
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'UMENOS'),
)

# Gramática
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion'''

def p_instrucciones_evaluar(t):
    'instruccion : REVALUAR CORIZQ expresion CORDER PTCOMA'
    print('El valor de la expresión es:', t[3])

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion : ENTERO
                 | DECIMAL'''
    t[0] = float(t[1]) if '.' in str(t[1]) else int(t[1])

# Error sintáctico
def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

# Crear el parser
parser = yacc.yacc()

# Leer y analizar el archivo de entrada
with open("entrada.txt", "r") as f:
    input = f.read()
    print("Contenido del archivo:", input)
    parser.parse(input)

