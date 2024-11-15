import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'IDENTIFIER', 'LITERAL_NUM', 'MAS', 'MENOS', 'POR', 'DIVIDIDO', 
    'PARIZQ', 'PARDER', 'PTCOMA', 'IGUAL', 'MENORQUE', 'MAYORQUE', 
    'MENORIGUAL', 'MAYORIGUAL', 'IGUALDAD', 'LLAVEIZQ', 'LLAVEDER'
]

# Palabras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE'
}

tokens += list(reserved.values())

# Definiciones de tokens
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PTCOMA = r';'
t_IGUAL = r'='
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUALDAD = r'=='
t_ignore = ' \t'

# Token de número literal
def t_LITERAL_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Token de identificador y palabras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Seguimiento de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construye el lexer
lexer = lex.lex()

# Diccionario para almacenar valores de variables
variables = {}

# Clases para representar el árbol sintáctico
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

    def evaluate(self):
        left_val = self.left if isinstance(self.left, int) else variables.get(self.left, 0)
        right_val = self.right if isinstance(self.right, int) else variables.get(self.right, 0)
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val

class ConditionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

    def evaluate(self):
        left_val = self.left if isinstance(self.left, int) else variables.get(self.left, 0)
        right_val = self.right if isinstance(self.right, int) else variables.get(self.right, 0)
        if self.operator == '<':
            return left_val < right_val
        elif self.operator == '>':
            return left_val > right_val
        elif self.operator == '<=':
            return left_val <= right_val
        elif self.operator == '>=':
            return left_val >= right_val
        elif self.operator == '==':
            return left_val == right_val

class IfNode(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def __str__(self):
        result = f"if {self.condition} {{ {self.if_block} }}"
        if self.else_block:
            result += f" else {{ {self.else_block} }}"
        return result

    def execute(self):
        if self.condition.evaluate():
            execute_block(self.if_block)
        elif self.else_block:
            execute_block(self.else_block)

# Definición de la gramática
def p_programa(t):
    '''programa : programa instruccion
                | instruccion'''
    if len(t) == 3:
        t[0] = t[1] + [t[2]] if isinstance(t[1], list) else [t[1], t[2]]
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion : if_statement
                   | asignacion'''
    t[0] = t[1]

def p_if_statement(t):
    '''if_statement : IF PARIZQ condicion PARDER LLAVEIZQ bloque LLAVEDER ELSE LLAVEIZQ bloque LLAVEDER
                    | IF PARIZQ condicion PARDER LLAVEIZQ bloque LLAVEDER'''
    if len(t) == 12:
        t[0] = IfNode(t[3], t[6], t[10])
    else:
        t[0] = IfNode(t[3], t[6])

def p_condicion(t):
    '''condicion : expresion MENORQUE expresion
                 | expresion MAYORQUE expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion
                 | expresion IGUALDAD expresion'''
    t[0] = ConditionNode(t[1], t[2], t[3])

def p_asignacion(t):
    '''asignacion : IDENTIFIER IGUAL expresion PTCOMA'''
    variables[t[1]] = t[3].evaluate() if isinstance(t[3], BinaryOpNode) else t[3]
    t[0] = f"{t[1]} = {variables[t[1]]}"

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion'''
    t[0] = BinaryOpNode(t[1], t[2], t[3])

def p_expresion_num(t):
    '''expresion : LITERAL_NUM'''
    t[0] = t[1]

def p_expresion_variable(t):
    '''expresion : IDENTIFIER'''
    t[0] = t[1]

def p_bloque(t):
    '''bloque : instruccion
              | bloque instruccion'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]

def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}' en la línea {t.lineno}")
    else:
        print("Error sintáctico al final del archivo")

# Función para ejecutar bloques
def execute_block(block):
    if isinstance(block, list):
        for instr in block:
            if isinstance(instr, IfNode):
                instr.execute()
            else:
                pass  # Las asignaciones ya están manejadas

# Construye el parser
parser = yacc.yacc()

# Ejemplo de prueba
input_text = '''
x = 12;
if (x < 10) {
    y = 5;
} else {
    y = 20;
}
'''

# Realiza el parsing y ejecuta el código
parse_tree = parser.parse(input_text)
print("Parse Tree:", parse_tree)
print("Variable values:", variables)
