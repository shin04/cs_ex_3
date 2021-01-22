#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

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
while_first_label = -1

for_undifined_label = -1
for_first_label = -1
for_cond_var = Factor(Scope.LOCAL)

if_undifined_label = -1
if_first_label = -1
else_undifined_label = -1
EXIST_ELSE = False

RESULT_FILE_NAME = 'result'

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
    'function': 'FUNCTION',
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

    file_path = ''
    # 中間コードのファイル書き出し
    if RESULT_FILE_NAME == 'result':
        file_path = RESULT_FILE_NAME+".ll"
    else:
        file_path = "../results/"+RESULT_FILE_NAME+".ll"

    with open(file_path, "w") as fout:
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
                 | func_decl
    '''


def p_func_decl(p):
    '''
    func_decl : FUNCTION proc_name SEMICOLON inblock
              | FUNCTION proc_name LPAREN args_flag id_list args_action RPAREN SEMICOLON inblock
    '''


def p_proc_decl(p):
    '''
    proc_decl : PROCEDURE proc_name SEMICOLON inblock
              | PROCEDURE proc_name LPAREN args_flag id_list args_action RPAREN SEMICOLON inblock
    '''


def p_args_flag(p):
    '''
    args_flag :
    '''

    symbols.is_args = True


def p_args_action(p):
    '''
    args_action :
    '''

    # 戻り値があるならレジスタを確保
    if p[-5] == 'function':
        retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
        alloca_code = llvmcodes.LLVMCodeAlloca(retval)
        codelist.append(alloca_code)
        functions[-1].retval = retval

    # factorstackには引数しか入っていない（はず）
    # factorstackの値を全て取り出して、arglistにぶち込む
    # ついでにalloca & store

    c_args = len(factorstack)

    for i in range(c_args):
        # arglistにぶっこむ
        arg = factorstack.pop()
        arg.val -= 1
        functions[-1].arglist.append('i32')

        # alloca
        retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
        alloca_code = llvmcodes.LLVMCodeAlloca(retval)
        codelist.append(alloca_code)

        # store
        store_code = llvmcodes.LLVMCodeStore(arg, retval)
        codelist.append(store_code)

    symbols.is_args = False


def p_proc_name(p):
    '''
    proc_name : IDENT
    '''

    # 手続き宣言時にコードリストのリセット
    global codelist, factorstack
    functions[-1].codes = codelist
    codelist = []
    factorstack = []

    res = symbols.insert(p[1], Scope.FUNC)
    symbols.is_func = True
    print('INSERT', res)

    func = Fundecl(p[1])
    if p[-1] == 'function':
        func.rettype = 'i32'
    functions.append(func)


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

    global while_first_label
    while_first_label = label_val

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
    arg2 = Factor(vtype=res[2], vname=res[0], val=res[1])  # 命令の第2引数
    l = llvmcodes.LLVMCodeStore(arg1, arg2)  # 命令を生成
    codelist.append(l)  # 命令列の末尾に追加

    print(l)


def p_if_statement(p):
    '''
    if_statement : IF condition if_action_1 THEN statement else_statement
    '''

    symbols.is_else_block = False


def p_if_action_1(p):
    '''
    if_action_1 :
    '''

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())
    retval = factorstack.pop()
    l = llvmcodes.LLVMCodeBrCond(retval, label_val, 'undifined')
    codelist.append(l)

    global if_undifined_label
    if_undifined_label = len(codelist)-1

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


def p_else_statement(p):
    '''
    else_statement : ELSE else_action_1 statement
                   |
    '''

    if (len(p) > 1):
        # elseがある
        label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())

        if else_undifined_label != -1:
            l = codelist[else_undifined_label]
            arg1 = label_val
            codelist[else_undifined_label] = llvmcodes.LLVMCodeBrUncond(arg1)

        l = llvmcodes.LLVMCodeBrUncond(label_val)
        codelist.append(l)

        l = llvmcodes.LLVMCodeLabel(label_val)
        codelist.append(l)
    else:
        label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())

        if if_undifined_label != -1:
            l = codelist[if_undifined_label]
            arg1 = l.arg1
            arg2 = l.arg2
            arg3 = label_val
            codelist[if_undifined_label] = llvmcodes.LLVMCodeBrCond(arg1, arg2, arg3)

        l = llvmcodes.LLVMCodeBrUncond(label_val)
        codelist.append(l)

        l = llvmcodes.LLVMCodeLabel(label_val)
        codelist.append(l)


def p_else_action_1(p):
    '''
    else_action_1 :
    '''

    symbols.is_block = True
    symbols.is_else_block = True

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())

    if if_undifined_label != -1:
        l = codelist[if_undifined_label]
        arg1 = l.arg1
        arg2 = l.arg2
        arg3 = label_val
        codelist[if_undifined_label] = llvmcodes.LLVMCodeBrCond(arg1, arg2, arg3)

    if p[-1]:
        l = llvmcodes.LLVMCodeBrUncond('undifined')
        global else_undifined_label
        else_undifined_label = len(codelist)
    else:
        l = llvmcodes.LLVMCodeBrUncond(label_val)
    codelist.append(l)

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


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

    l = llvmcodes.LLVMCodeBrUncond(while_first_label)
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
    for_statement : FOR IDENT ASSIGN expression for_action_1 TO expression for_action_3 DO for_action_2 statement
    '''

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())
    l = llvmcodes.LLVMCodeBrUncond(label_val)
    codelist.append(l)
    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)

    res = symbols.lookup(p[2])
    arg1 = Factor(Scope.LOCAL, val=functions[-1].get_register())
    arg2 = Factor(vtype=res[2], vname=res[0], val=res[1])
    l = llvmcodes.LLVMCodeLoad(arg1, arg2)
    codelist.append(l)
    factorstack.append(arg2)
    factorstack.append(arg1)

    retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
    arg1 = factorstack.pop()
    arg2 = Factor(Scope.CONSTANT, val=1)
    l = llvmcodes.LLVMCodeAdd(arg1, arg2, retval)
    codelist.append(l)
    factorstack.append(retval)

    arg1 = factorstack.pop()
    arg2 = factorstack.pop()
    l = llvmcodes.LLVMCodeStore(arg1, arg2)
    codelist.append(l)

    # ----------

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())

    if for_undifined_label != -1:
        l = codelist[for_undifined_label]
        arg1 = l.arg1
        arg2 = l.arg2
        arg3 = label_val
        codelist[for_undifined_label] = llvmcodes.LLVMCodeBrCond(arg1, arg2, arg3)

    l = llvmcodes.LLVMCodeBrUncond(for_first_label)
    codelist.append(l)

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


def p_for_action_1(p):
    '''
    for_action_1 :
    '''

    res = symbols.lookup(p[-3])
    print('LOOKUP for', res)

    arg1 = factorstack.pop()
    arg2 = Factor(vtype=res[2], vname=res[0], val=res[1])

    l = llvmcodes.LLVMCodeStore(arg1, arg2)
    codelist.append(l)

    factorstack.append(arg2)


def p_for_action_2(p):
    '''
    for_action_2 :
    '''

    symbols.is_block = True


def p_for_action_3(p):
    '''
    for_action_3 :
    '''

    global for_undifined_label, for_first_label

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())
    l_br = llvmcodes.LLVMCodeBrUncond(label_val)
    codelist.append(l_br)

    for_first_label = label_val

    l_label = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l_label)

    arg1 = Factor(Scope.LOCAL, val=functions[-1].get_register())
    l_icmp_arg2 = factorstack.pop()  # 次のicmp用の引数
    arg2 = factorstack.pop()
    l_load = llvmcodes.LLVMCodeLoad(arg1, arg2)
    codelist.append(l_load)
    factorstack.append(arg1)

    cmptype = llvmcodes.CmpType.SLT
    arg1 = factorstack.pop()
    retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
    l_icmp = llvmcodes.LLVMCodeIcmp(cmptype, arg1, l_icmp_arg2, retval)
    codelist.append(l_icmp)

    factorstack.append(retval)

    label_val = Factor(Scope.LOCAL, val=functions[-1].get_register())
    retval = factorstack.pop()
    l = llvmcodes.LLVMCodeBrCond(retval, label_val, 'undifined')
    codelist.append(l)

    for_undifined_label = len(codelist)-1

    l = llvmcodes.LLVMCodeLabel(label_val)
    codelist.append(l)


def p_proc_call_statement(p):
    '''
    proc_call_statement : proc_call_name set_args
                        | proc_call_name LPAREN arg_list RPAREN set_args
    '''


def p_set_args(p):
    '''
    set_args :
    '''

    args = []
    while True:
        fact = factorstack.pop()
        if fact.type == Scope.FUNC:
            break
        else:
            args.append(('%' + str(fact.val), 'i32'))

    print(fact.ret)
    if not fact.ret:
        # 戻り値なし
        l = llvmcodes.LLVMCodeProcCall('void', fact, args)
        codelist.append(l)
    else:
        # 戻り値あり
        reg = Factor(Scope.LOCAL, val=functions[-1].get_register())
        l = llvmcodes.LLVMCodeProcCall('void', fact, args, reg=reg)
        codelist.append(l)

    factorstack.append(fact)


def p_proc_call_name(p):
    '''
    proc_call_name : IDENT
    '''

    res = symbols.lookup(p[1])
    print('LOOKUP', res)

    func = Factor(Scope.FUNC, vname=res[0])
    for f in functions:
        if f.name == res[0]:
            func.ret = True
    factorstack.append(func)


def p_block_statement(p):
    '''
    block_statement : BEGIN begin_action_1 statement_list END
    '''

    def end_proc():
        global factorstack, codelist

        # return文
        func = functions[-1]
        rtype = func.rettype
        rval = func.retval
        if rval.val != 0:
            retval = Factor(Scope.LOCAL, val=func.get_register())
            load_code = llvmcodes.LLVMCodeLoad(retval, rval)
            codelist.append(load_code)
            rval = retval
        ret_code = llvmcodes.LLVMCodeRet(rtype, rval)
        codelist.append(ret_code)

        # コードリストのリセット
        functions[-1].codes = codelist
        codelist = []
        factorstack = []

    if symbols.is_block:
        if not symbols.is_else_block:
            symbols.is_block = False
        # 手続きの終了
        if symbols.is_func and not symbols.is_else_block:
            symbols.is_func = False
            res = symbols.delete()
            print('DELETE', res)

            end_proc()

    else:
        end_proc()


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

    retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
    proc_type = 'i32'
    proc = 'scanf'
    var_type = 'i32*'
    var = Factor(res[2], res[0], res[1])
    l = llvmcodes.LLVMCodeOutProcCall(retval, proc_type, proc, var_type, var)
    codelist.append(l)

    l = '@.str = private unnamed_addr constant [3 x i8] c\"%d\\00\", align 1'
    functions[0].codes.insert(0, l)

    functions[-1].use_read = llvmcodes.LLVMCodeDeclare(proc_type, proc)


def p_write_statemtnt(p):
    '''
    write_statement : WRITE LPAREN expression RPAREN
    '''

    retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
    proc_type = 'i32'
    proc = 'printf'
    var_type = 'i32'
    var = factorstack.pop()
    l = llvmcodes.LLVMCodeOutProcCall(retval, proc_type, proc, var_type, var)
    codelist.append(l)

    functions[-1].use_write = llvmcodes.LLVMCodeDeclare(proc_type, proc)


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
    elif p[2] == '<':
        cmptype = llvmcodes.CmpType.SLT
    elif p[2] == '=':
        cmptype = llvmcodes.CmpType.EQUAL
    elif p[2] == '<>':
        cmptype = llvmcodes.CmpType.NE
    elif p[2] == '>=':
        cmptype = llvmcodes.CmpType.SGE
    elif p[2] == '<=':
        cmptype = llvmcodes.CmpType.SLE
    arg2 = factorstack.pop()
    arg1 = factorstack.pop()
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

               | proc_call_name LPAREN arg_list RPAREN set_args
               | PLUS proc_call_name LPAREN arg_list RPAREN set_args
               | MINUS proc_call_name LPAREN arg_list RPAREN set_args
               | expression PLUS proc_call_name LPAREN arg_list RPAREN set_args
               | expression MINUS proc_call_name LPAREN arg_list RPAREN set_args
    '''

    if len(p) == 3:
        # 右辺が2個の場合
        if p[1] == '+':
            # termと同じ処理
            pass
        elif p[1] == '-':
            # 符号を反転
            fact = factorstack.pop()
            if fact.val != None:
                fact.val = -fact.val
            factorstack.append(fact)
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

         | proc_call_name LPAREN arg_list RPAREN set_args MULT factor
         | proc_call_name LPAREN arg_list RPAREN set_args DIV factor
    '''

    if len(p) in [4, 8]:
        index = len(p) - 2
        arg2 = factorstack.pop()
        arg1 = factorstack.pop()
        retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
        if p[index] == "*":
            l = llvmcodes.LLVMCodeMul(arg1, arg2, retval)
        elif p[index] == "div":
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

    count = symbols.countup(p[1])
    if count != 1:
        res = symbols.lookup(p[1], Scope.LOCAL)
    else:
        res = symbols.lookup(p[1])
    print('LOOKUP', res)

    if count != 1:
        val = res[1] + 1
    else:
        val = res[1]

    arg2 = Factor(vtype=res[2], vname=res[0], val=val)  # 命令の第2引数
    retval = Factor(Scope.LOCAL, val=functions[-1].get_register())
    if not symbols.is_args:
        l = llvmcodes.LLVMCodeLoad(retval, arg2)  # 命令を生成
        codelist.append(l)  # 命令列の末尾に追加
    factorstack.append(retval)  # Loadの結果をスタックにプッシュ


def p_arg_list(p):
    '''
    arg_list : expression
             | arg_list COMMA expression
    '''

    # symbols.is_args = False


def p_id_list(p):
    '''
    id_list : IDENT
            | id_list COMMA IDENT
    '''

    var_name = ''
    var_address = 0
    scope = Scope.LOCAL if symbols.is_func else Scope.GLOBAL

    if p[1] == None:
        index = 3
    else:
        index = 1

    var_name = p[index]

    if symbols.is_func:
        var_address = functions[-1].get_register()
        retval = Factor(Scope.LOCAL, val=var_address)
        if not symbols.is_args:
            l = llvmcodes.LLVMCodeAlloca(retval)
            codelist.append(l)
        factorstack.append(retval)
    else:
        retval = Factor(Scope.GLOBAL, var_name)
        l = llvmcodes.LLVMCodeGlobal(retval)
        codelist.append(l)
        factorstack.append(retval)

    res = symbols.insert(var_name, scope, var_address)
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

    pattern = '.*/(.*).p$'
    result = re.match(pattern, sys.argv[1])
    RESULT_FILE_NAME = result.group(1)
    print(RESULT_FILE_NAME)

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
