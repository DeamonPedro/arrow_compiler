from ply import yacc
from arrow_lex import *
from arrow_semantic import *

precedence = (
    ('right', 'INTERROGATION'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'DIFF'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)


def p_program(p):
    ''' program : decSeq'''
    p[0] = Program(dec_seq=p[1])


def p_dec(p):
    '''
    dec : varDec
        | FUNC ID LPAREN paramList RPAREN ARROW LBRACE block RBRACE
        | FUNC type ID LPAREN paramList RPAREN ARROW LBRACE block RBRACE
    '''
    if len(p) == 2:
        p[0] = Dec(var_dec=p[1])
    elif len(p) == 10:
        p[0] = Dec(id_=p[2], param_list=p[4], block=p[8])
    elif len(p) == 11:
        p[0] = Dec(type_=p[2], id_=p[3], param_list=p[5], block=p[9])


def p_var_dec(p):
    '''varDec : type varSpecSeq SEMICOLON'''
    p[0] = VarDec(type_=p[1], var_spec_seq=p[2])


def p_var_spec(p):
    '''
    varSpec : ID
            | ID ASSIGN literal
            | ID LCOLC NUMBER RCOLC
            | ID LCOLC NUMBER RCOLC ASSIGN LBRACE literalSeq RBRACE
    '''
    if len(p) == 2:
        p[0] = VarSpec(id_=p[1])
    elif len(p) == 4:
        p[0] = VarSpec(id_=p[1], literal=p[3])
    elif len(p) == 5:
        p[0] = VarSpec(id_=p[1], number=p[3])
    elif len(p) == 9:
        p[0] = VarSpec(id_=p[1], number=p[3], literal_seq=p[7])


def p_type(p):
    '''
    type : NUMBER
         | STRING
         | BOOL
    '''
    p[0] = Type(type_=p[1])


def p_param(p):
    '''
    param : type ID
          | type ID LCOLC RCOLC
    '''
    if len(p) == 3:
        p[0] = Param(type_=p[1], id_=p[2], array=False)
    elif len(p) == 5:
        p[0] = Param(type_=p[1], id_=p[2], array=True)


def p_block(p):
    ''' block : varDecList stmtList'''
    p[0] = Block(var_dec_list=p[1], stmt_list=p[2])


def p_stmt(p):
    '''
      stmt : ifStmt
           | whileStmt
           | forStmt
           | breakStmt
           | returnStmt
           | readStmt
           | writeStmt
           | assign SEMICOLON
           | subCall SEMICOLON
    '''
    p[0] = Stmt(stmt=p[1])


def p_if_stmt(p):
    '''
    ifStmt : IF LPAREN exp RPAREN ARROW LBRACE block RBRACE
           | IF LPAREN exp RPAREN ARROW RBRACE block RBRACE ELSE LBRACE block RBRACE
    '''
    if len(p) == 8:
        p[0] = IfStmt(if_=p[1], exp=p[3], block1=p[7])
    if len(p) == 12:
        p[0] = IfStmt(if_=p[1], exp=p[3], block1=p[7],
                      else_=p[9], block2=p[11])


def p_while_stmt(p):
    ''' whileStmt : WHILE LPAREN exp RPAREN ARROW LBRACE block RBRACE '''
    p[0] = WhileStmt(while_=p[1], exp=p[3], block=p[7])


def p_for_stmt(p):
    '''forStmt : FOR LPAREN assign SEMICOLON exp SEMICOLON assign RPAREN ARROW LBRACE block RBRACE'''
    p[0] = ForStmt(for_=p[1], assign1=p[3], exp=p[5],
                   assign2=p[7], block=p[11])


def p_break_stmt(p):
    '''breakStmt : BREAK SEMICOLON'''
    p[0] = BreakStmt(break_=p[1])


def p_read_stmt(p):
    '''readStmt : READ var SEMICOLON'''
    p[0] = ReadStmt(read=p[1], var=p[2])


def p_write_stmt(p):
    '''writeStmt : WRITE expList SEMICOLON'''
    p[0] = WriteStmt(write=p[1], exp_list=p[2])


def p_return_stmt(p):
    '''
    returnStmt : RETURN SEMICOLON
               | RETURN exp SEMICOLON
    '''
    if len(p) == 3:
        p[0] = ReturnStmt(return_=p[1])
    if len(p) == 4:
        p[0] = ReturnStmt(return_=p[1], exp=p[2])


def p_sub_call(p):
    '''subCall : ID LPAREN expList RPAREN'''
    p[0] = SubCall(id_=p[1], exp_list=p[3])


def p_assign(p):
    '''
    assign : var ASSIGN exp
           | var PLUS_EQ exp
           | var MINUS_EQ exp
           | var MULTIPLY_EQ exp
           | var DIVIDE_EQ exp
           | var MOD exp
    '''
    p[0] = Assign(op=p[2], left=p[1], right=p[3])


def p_var(p):
    '''
    var : ID
        | ID LCOLC exp RCOLC
    '''
    if len(p) == 2:
        p[0] = Variable(id_=p[1])
    else:
        p[0] = Variable(id_=p[1], exp=p[3])


def p_exp(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULTIPLY exp
        | exp DIVIDE exp
        | exp MOD exp
        | exp EQ exp
        | exp DIFF exp
        | exp LE exp
        | exp GE exp
        | exp GT exp
        | exp LT exp
        | exp AND exp
        | exp OR exp
        | NOT exp
        | MINUS exp
        | exp INTERROGATION exp COLON exp
        | subCall
        | var
        | literal
        | LPAREN exp RPAREN
        | param
    '''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = Exp(op=p[2])
        else:
            p[0] = Exp(op=p[2], left=p[1], right=p[3])
    elif len(p) == 3:
        p[0] = Exp(op=p[1], right=p[2])
    elif len(p) == 2:
        p[0] = Exp(op=p[1])
    elif len(p) == 6:
        p[0] = Exp(op=p[1], left=p[3], right=p[5])


def p_literal(p):
    '''
    literal : CONST_NUMBER
            | CONST_STRING
            | TRUE
            | FALSE
    '''
    p[0] = Literal(literal=p[1])


def p_param_list(p):
    '''
    paramList : paramSeq
              | empty
    '''
    p[0] = ParamList(param_seq=p[1])


def p_param_seq(p):
    '''
    paramSeq : param COMMA paramSeq
             | param
    '''
    if len(p) == 4:
        p[0] = ParamSeq(param=p[1], param_seq=p[3])
    elif len(p) == 2:
        p[0] = ParamSeq(param=p[1])


def p_var_dec_list(p):
    '''
    varDecList : varDec varDecList
               | empty
    '''
    if p[1]:
        p[0] = VarDecList(var_dec=p[1], var_dec_list=p[2])


def p_var_spec_seq(p):
    '''
    varSpecSeq : varSpec COMMA varSpecSeq
               | varSpec
    '''
    if len(p) == 4:
        p[0] = VarSpecSeq(var_spec=p[1], var_spec_seq=p[3])
    elif len(p) == 2:
        p[0] = VarSpecSeq(var_spec=p[1])


def p_exp_list(p):
    '''
    expList : expSeq
            | empty
    '''
    if p[1]:
        p[0] = ExpList(exp_seq=p[1])


def p_literal_seq(p):
    '''
    literalSeq : literal COMMA literalSeq
               | literal
    '''
    if len(p) == 4:
        p[0] = LiteralSeq(literal=p[1], literal_seq=p[3])
    elif len(p) == 2:
        p[0] = LiteralSeq(literal=p[1])


def p_stmt_list(p):
    '''
    stmtList : stmt stmtList
             | empty
    '''
    if p[1]:
        p[0] = StmtList(stmt=p[1], stmt_list=p[2])


def p_dec_seq(p):
    '''
    decSeq : dec decSeq
           | dec
    '''
    if len(p) == 2:
        p[0] = DecSeq(dec=p[1])
    elif len(p) == 3:
        p[0] = DecSeq(dec=p[1], dec_seq=p[2])


def p_exp_seq(p):
    '''
    expSeq : exp COMMA expSeq
           | exp
    '''
    if len(p) == 2:
        p[0] = ExpSeq(exp=p[1])
    elif len(p) == 4:
        p[0] = ExpSeq(exp=p[1], exp_seq=p[3])


def p_empty(p):
    ''' empty : '''
    pass


def p_error(p):
    last_cr = p.lexer.lexdata.rfind('\n', 0, p.lexer.lexpos)
    column = p.lexer.lexpos - last_cr - 1

    if p:
        print("Erro de sintaxe em {0} na linha {1} coluna {2}".format(
            p.value, p.lexer.lineno, column))
    else:
        print("Erro de sintaxe EOF")


parser = yacc.yacc()
