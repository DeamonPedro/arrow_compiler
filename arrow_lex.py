import ply.lex as lex

reserved = {
    'bool'	:	'BOOL',
    'break'	:	'BREAK',
    'for'	:	'FOR',
    'if'	:	'IF',
    'else'	:	'ELSE',
    'num'	:	'NUMBER',
    'return':	'RETURN',
    'str':	'STRING',
    'true'	:	'TRUE',
    'false'	:	'FALSE',
    'while'	:	'WHILE',
    'write':	'WRITE',
    'read': 	'READ',
    'func': 'FUNC'
}


tokens = [
    'ID',
    'CONST_STRING',
    'CONST_NUMBER',
    'PLUS',
    'ARROW',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'ASSIGN',
    'RPAREN',
    'LPAREN',
    'RCOLC',
    'LCOLC',
    'RBRACE',
    'LBRACE',
    'COMMA',
    'SEMICOLON',
    'OR',
    'AND',
    'NOT',
    'INTERROGATION',
    'COLON',
    'EQ',
    'DIFF',
    'LT',
    'GT',
    'LE',
    'GE',
    'PLUS_EQ',
    'MINUS_EQ',
    'MULTIPLY_EQ',
    'DIVIDE_EQ',
    'MOD',
] + list(reserved.values())

# OPCIONAIS
t_ARROW = r'->'
t_RPAREN = r'\)'
t_LPAREN = r'\('
t_RCOLC = r'\]'
t_LCOLC = r'\['
t_RBRACE = r'\}'
t_LBRACE = r'\{'
t_COMMA = r','
t_SEMICOLON = r';'

# OPERATORS
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'OR'
t_AND = r'AND'
t_NOT = r'NOT'
t_ASSIGN = r'<-'
t_EQ = r'=='
t_DIFF = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_PLUS_EQ = r'\+='
t_MINUS_EQ = r'-='
t_MULTIPLY_EQ = r'\*='
t_DIVIDE_EQ = r'/='
t_INTERROGATION = r'\?'
t_COLON = r':'

t_ignore = " \t\v\r"


def t_CONST_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor inteiro muito grande %d", t.value)
        t.value = 0
    return t


def t_CONST_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    column = find_column(t.lexer.lexdata, t)
    print('LexError(%s,%r,%d,%d)' % (t.type, t.value, t.lineno, column))
    t.lexer.skip(1)


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_comment_multiline(t):
    r'((//.*)|(/\*(.|\n)*\*/))'
    pass


def find_column(input, token):
    last_cr = input.rfind('\n', 0, lex.lexer.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (lex.lexer.lexpos - last_cr) + 1
    return column


lexer = lex.lex()
