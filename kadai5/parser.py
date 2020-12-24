#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import ply.lex as lex
import ply.yacc as yacc

from symtab import Scope, SymbolTable
from decls import Fundecl, Factor
import llvmcodes

symbols = SymbolTable()
factorstack = []
functions = []
codelist = []
labels = []
while_undifined_label = -1

# トークン定義
tokens = (
    'BEGIN', 'DIV', 'DO', 'ELSE', 'END', 'FOR', 'FORWARD', 'FUNCTION', 'IF', 'PROCEDURE', 'PROGRAM',
    'READ', 'THEN', 'TO', 'VAR', 'WHILE', 'WRITE',
    'PLUS', 'MINUS', 'MULT', 'EQ', 'NEQ', 'LE', 'LT', 'GE', 'GT', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA',
    'SEMICOLON', 'COLON', 'INTERVAL', 'PERIOD', 'NUMBER', 'IDENT', 'ASSIGN'
)

# 予約語
reserved = {
    'begin': 'BEGIN',
    'div': 'DIV',
    'do': 'DO',
    'else': 'ELSE',
    'end': 'END',
    'for': 'FOR',
    'forward': 'FORWARD',
    'fucntion': 'FUNCTION',
    'if': 'IF',
    'procedure': 'PROCEDURE',
    'program': 'PROGRAM',
    'read': 'READ',
    'then': 'THEN',
    'to': 'TO',
    'var': 'VAR',
    'while': 'WHILE',
    'write': 'WRITE'
}

# 正規表現
t_PLUS = r'\+'
t_MINUS = '-'
t_MULT = r'\*'
t_EQ = '='
t_NEQ = '<>'
t_LE = '<='
t_LT = '<'
t_GE = '>='
t_GT = '>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = '{'
t_RBRACKET = '}'
t_COMMA = ','
t_SEMICOLON = ';'
t_COLON = ':'
t_INTERVAL = r'\.\.'
t_PERIOD = '.'
t_ASSIGN = ':='

t_ignore_COMMENT = r'\#.*'
t_ignore = ' \t'


def t_IDENT(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_NUMBER(t):
    r'[1-9][0-9]*|0'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Line %d: integer value %s is too large" % t.lineno, t.value)
        t.value = 0
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("不正な文字", t.value[0])
    t.lexer.skip(1)

#################################################################
# ここから先に構文規則を書く
#################################################################


def p_program(p):
    '''
    program : PROGRAM IDENT SEMICOLON outblock PERIOD
    '''

    # for f in functions:
    #     for c in f.codes:
    #         print(c)

    # 中間コードのファイル書き出し
    with open("result.ll", "w") as fout:
        for f in functions:
            f.print(fout)


def p_outblock(p):
    '''
    outblock : var_decl_part subprog_decl_part statement
    '''


def p_var_decl_part(p):
    '''
    var_decl_part : var_decl_list SEMICOLON
                  |
    '''


def p_var_decl_list(p):
    '''
    var_decl_list : var_decl_list SEMICOLON var_decl
                  | var_decl
    '''


def p_var_decl(p):
    '''
    var_decl : VAR id_list
    '''


def p_subprog_decl_part(p):
    '''
    subprog_decl_part : subprog_decl_list SEMICOLON
                      |
    '''


def p_subprog_decl_list(p):
    '''
    subprog_decl_list : subprog_decl_list SEMICOLON subprog_decl
                      | subprog_decl
    '''


def p_subprog_decl(p):
    '''
    subprog_decl : proc_decl
    '''


def p_proc_decl(p):
    '''
    proc_decl : PROCEDURE proc_name SEMICOLON inblock
    '''


def p_proc_name(p):
    '''
    proc_name : IDENT
    '''

    res = symbols.insert(p[1], Scope.FUNC)
    symbols.is_func = True
    print('INSERT', res)

    func = Fundecl(p[1])
    functions.append(p[1])


def p_inblock(p):
    '''
    inblock : var_decl_part statement
    '''


def p_statement_list(p):
    '''
    statement_list : statement_list SEMICOLON statement
                   | statement
    '''


def p_statement(p):
    '''
    statement : assignment_statement
              | if_statement
              | statement_action_1 while_statement
              | for_statement
              | proc_call_statement
              | null_statement
              | block_statement
              | read_statement
              | write_statement
    '''


def p_statement_action_1(p):
    '''
    statement_action_1 : 
    '''

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())

    l = llvmcodes.LLVMCodeBrUncond(label_val)
    codelist.append(l)

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


def p_assignment_statement(p):
    '''
    assignment_statement : IDENT ASSIGN expression
    '''

    res = symbols.lookup(p[1])
    print('LOOKUP', res)

    arg1 = factorstack.pop()  # 命令の第1引数
    arg2 = Factor(vtype=res[2], vname=res[0])  # 命令の第2引数
    l = llvmcodes.LLVMCodeStore(arg1, arg2)  # 命令を生成
    codelist.append(l)  # 命令列の末尾に追加


def p_if_statement(p):
    '''
    if_statement : IF condition THEN statement else_statement
    '''


def p_else_statement(p):
    '''
    else_statement : ELSE statement
                   |
    '''


def p_while_statement(p):
    '''
    while_statement : WHILE condition while_action_2 DO while_action_1 statement
    '''

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())

    if while_undifined_label != -1:
        l = codelist[while_undifined_label]
        arg1 = l.arg1
        arg2 = l.arg2
        arg3 = label_val

        codelist[while_undifined_label] = llvmcodes.LLVMCodeBrCond(arg1, arg2, arg3)

    l = llvmcodes.LLVMCodeBrUncond(label_val)
    codelist.append(l)

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


def p_while_action_1(p):
    '''
    while_action_1 :
    '''

    symbols.is_block = True


def p_while_action_2(p):
    '''
    while_action_2 :
    '''

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())
    retval = factorstack.pop()
    l = llvmcodes.LLVMCodeBrCond(retval, label_val, 'undifined')
    codelist.append(l)

    global while_undifined_label
    while_undifined_label = len(codelist)-1

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


def p_for_statement(p):
    '''
    for_statement : FOR IDENT ASSIGN expression for_action_1 TO expression DO statement
    '''


def p_for_action_1(p):
    '''
    for_action_1 :
    '''

    res = symbols.lookup(p[-3])
    print('LOOKUP for', res)


def p_proc_call_statement(p):
    '''
    proc_call_statement : proc_call_name
    '''


def p_proc_call_name(p):
    '''
    proc_call_name : IDENT
    '''

    res = symbols.lookup(p[1])
    # symbols.is_func = True
    print('LOOKUP', res)


def p_block_statement(p):
    '''
    block_statement : BEGIN begin_action_1 statement_list END
    '''

    if symbols.is_block:
        symbols.is_block = False
    else:
        global codelist, factorstack

        # 手続きの終了
        if symbols.is_func:
            symbols.is_func = False
            res = symbols.delete()
            print('DELETE', res)

        # return文
        l = llvmcodes.LLVMCodeRet()
        codelist.append(l)

        # コードリストのリセット
        functions[-1].codes = codelist
        codelist = []
        factorstack = []


def p_begin_action_1(p):
    '''
    begin_action_1 :
    '''

    if not symbols.is_block:
        # 初めて手続きに入ったならコードリストのリセット
        if len(functions) == 1:
            global codelist, factorstack
            functions[-1].codes = codelist
            codelist = []
            factorstack = []

        # main関数かどうか判定
        isin_main = False
        for function in functions:
            if function.name == 'main':
                isin_main = True
                break
        if not symbols.is_func and not isin_main:
            # main関数をpush
            main_func = Fundecl('main')
            main_func.rettype = 'i32'
            functions.append(main_func)


def p_read_statemtnt(p):
    '''
    read_statement : READ LPAREN IDENT RPAREN
    '''

    res = symbols.lookup(p[3])
    print('LOOKUP', res)


def p_write_statemtnt(p):
    '''
    write_statement : WRITE LPAREN expression RPAREN
    '''


def p_null_statement(p):
    '''
    null_statement :
    '''


def p_condition(p):
    '''
    condition : expression EQ expression
              | expression NEQ expression
              | expression LE expression
              | expression LT expression
              | expression GE expression
              | expression GT expression
    '''

    if p[2] == '>':
        cmptype = llvmcodes.CmpType.SGT
        arg1 = factorstack.pop()
        arg2 = factorstack.pop()
        retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
        l = llvmcodes.LLVMCodeIcmp(cmptype, arg1, arg2, retval)
        codelist.append(l)
        factorstack.append(retval)


def p_expression(p):
    '''
    expression : term
               | PLUS term
               | MINUS term
               | expression PLUS term
               | expression MINUS term
    '''

    if len(p) == 3:
        # 右辺が2個の場合
        if p[1] == '+':  # PLUS
            print('hogehoge')
    elif len(p) == 4:
        # 右辺が3個の場合
        arg2 = factorstack.pop()  # 命令の第2引数をポップ
        arg1 = factorstack.pop()  # 命令の第1引数をポップ
        retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
        if p[2] == "+":  # PLUS
            l = llvmcodes.LLVMCodeAdd(arg1, arg2, retval)  # 命令を生成
        elif p[2] == "-":  # MINUS
            l = llvmcodes.LLVMCodeSub(arg1, arg2, retval)  # 命令を生成
        codelist.append(l)  # 命令列の末尾に追加
        factorstack.append(retval)  # 加算の結果をスタックにプッシュ


def p_term(p):
    '''
    term : factor
         | term MULT factor
         | term DIV factor
    '''

    if len(p) == 4:
        arg2 = factorstack.pop()
        arg1 = factorstack.pop()
        retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
        if p[2] == "*":
            l = llvmcodes.LLVMCodeMul(arg1, arg2, retval)
        elif p[2] == "/":
            l = llvmcodes.LLVMCodeSdiv(arg1, arg2, retval)
        codelist.append(l)
        factorstack.append(retval)


def p_factor(p):
    '''
    factor : var_name
           | NUMBER
           | LPAREN expression RPAREN
    '''

    if type(p[1]) == int:
        # scope = Scope.LOCAL if symbols.is_func else Scope.GLOBAL
        scope = Scope.CONSTANT
        fact = Factor(scope, val=p[1])
        factorstack.append(fact)


def p_var_name(p):
    '''
    var_name : IDENT
    '''

    res = symbols.lookup(p[1])
    print('LOOKUP', res)

    arg2 = Factor(vtype=res[2], vname=res[0])  # 命令の第2引数
    retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
    l = llvmcodes.LLVMCodeLoad(retval, arg2)  # 命令を生成
    codelist.append(l)  # 命令列の末尾に追加
    factorstack.append(retval)  # Loadの結果をスタックにプッシュ


def p_arg_list(p):
    '''
    arg_list : expression
             | arg_list COMMA expression
    '''


def p_id_list(p):
    '''
    id_list : IDENT
            | id_list COMMA IDENT
    '''

    scope = Scope.LOCAL if symbols.is_func else Scope.GLOBAL
    if p[1] == None:
        index = 3
    else:
        index = 1

    res = symbols.insert(p[index], scope)

    scope = Scope.LOCAL if symbols.is_func else Scope.GLOBAL
    retval = Factor(scope, p[index])
    l = llvmcodes.LLVMCodeGlobal(retval)
    codelist.append(l)
    factorstack.append(retval)

    print('INSERT', res)


def p_error(p):
    #################################################################
    # 構文解析エラー時の処理
    #################################################################

    if p:
        # p.type, p.value, p.linenoを使ってエラーの処理を書く
        print('[ERROR] type: {}, value: {}, line No.: {}'.format(p.type, p.value, p.lineno))


if __name__ == "__main__":
    #################################################################
    # メインの処理
    #################################################################
    lexer = lex.lex(debug=0)  # 字句解析器
    yacc.yacc()  # 構文解析器

    # 記号表
    symbols = SymbolTable()

    # グローバル変数用の関数をpush
    global_func = Fundecl('')
    functions.append(global_func)

    # ファイルを開いて
    data = open(sys.argv[1]).read()
    # 解析を実行
    yacc.parse(data, lexer=lexer)
