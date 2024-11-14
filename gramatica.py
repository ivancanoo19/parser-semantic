import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'IDENTIFIER',  # Identificadores
    'LITERAL_NUM',  # Literales numéricos
    'MAS', 'MENOS', 'POR', 'DIVIDIDO',  # Operadores matemáticos
    'PARIZQ', 'PARDER', 'CORIZQ', 'CORDER',  # Paréntesis y corchetes
    'PTCOMA', 'IGUAL',  # Punto y coma, asignación
]

# Definiciones de patrones de tokens
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PTCOMA = r';'
t_IGUAL = r'='
t_LITERAL_NUM = r'\d+'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_ignore = ' \t'

# Saltos de línea
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores en el lexer
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Clases de nodos para el árbol sintáctico
class Node:
    def __repr__(self):
        return str(self)

class BinaryOpNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

class UnaryOpNode(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"({self.operator}{self.operand})"

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class VariableNode(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Variable:
    def __init__(self, name, value, data_type):
        self.name = name
        self.value = value
        self.data_type = data_type

# Variables globales para almacenar valores y tipos
variables = {}

# Función para evaluar nodos
def evaluate(node):
    if isinstance(node, NumberNode):
        return node.value
    elif isinstance(node, VariableNode):
        var = variables.get(node.name)
        if var:
            return var.value
        else:
            raise ValueError(f"Variable '{node.name}' no está definida.")
    elif isinstance(node, UnaryOpNode):
        return -evaluate(node.operand)
    elif isinstance(node, BinaryOpNode):
        left_val = evaluate(node.left)
        right_val = evaluate(node.right)
        if node.operator == '+':
            return left_val + right_val
        elif node.operator == '-':
            return left_val - right_val
        elif node.operator == '*':
            return left_val * right_val
        elif node.operator == '/':
            if right_val == 0:
                raise ValueError("Error: División por cero.")
            return left_val / right_val

# Gramática y reglas
def p_programa(t):
    '''programa : programa instruccion
                | instruccion'''
    pass

def p_instruccion(t):
    '''instruccion : declaracion_variable
                   | asignacion'''
    pass

def p_declaracion_variable(t):
    '''declaracion_variable : IDENTIFIER IGUAL expresion PTCOMA'''
    var_name = t[1]
    value = evaluate(t[3])
    data_type = 'int' if isinstance(value, int) else 'float'
    variables[var_name] = Variable(var_name, value, data_type)
    print(f"Variable declarada: {var_name} de tipo {data_type} = {value}")

def p_asignacion(t):
    '''asignacion : IDENTIFIER IGUAL expresion PTCOMA'''
    var_name = t[1]
    value = evaluate(t[3])
    if var_name in variables:
        variables[var_name].value = value
        print(f"Variable '{var_name}' actualizada con valor {value}")
    else:
        print(f"Error: La variable '{var_name}' no está declarada.")

def p_expresion_variable(t):
    'expresion : IDENTIFIER'
    if t[1] in variables:
        t[0] = VariableNode(t[1])
    else:
        raise ValueError(f"Error: La variable '{t[1]}' no está definida.")

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion'''
    t[0] = BinaryOpNode(t[1], t[2], t[3])

def p_expresion_unaria(t):
    'expresion : MENOS expresion'
    t[0] = UnaryOpNode('-', t[2])

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_corchetes(t):
    'expresion : CORIZQ expresion CORDER'
    t[0] = t[2]

def p_expresion_number(t):
    'expresion : LITERAL_NUM'
    t[0] = NumberNode(int(t[1]))

# Error sintáctico
def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}' en la línea {t.lineno}")
    else:
        print("Error sintáctico al final del archivo")

# Crear lexer y parser
lexer = lex.lex()
parser = yacc.yacc(debug=True)  # Activando debug para ver el proceso de análisis

# Análisis de entrada
def parse_input(input_text):
    input_text = input_text.strip()
    lexer.input(input_text)
    return parser.parse(input_text)

# Ejemplo de prueba
input_text = '''
x = 10;
y = 5;
z = x + y * 2;
'''

parse_input(input_text)
