import sys
from arrow_lex import lexer
from arrow_parser import parser
from arrow_semantic import *


if len(sys.argv) < 2:
    print("err: not input file")

input_file = open(sys.argv[1])
cod_input = input_file.read()

print(cod_input)
lexer.input(cod_input)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

program = parser.parse(cod_input)
if program:
    program.print_name()
    program.check_node()
