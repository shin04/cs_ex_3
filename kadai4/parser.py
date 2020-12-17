#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import ply.lex as lex
import ply.yacc as yacc

from symtab import Scope
from symtab import SymbolTable

symbols = SymbolTable()

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
              | while_statement
              | for_statement
              | proc_call_statement
              | null_statement
              | block_statement
              | read_statement
              | write_statement
    '''


def p_assignment_statement(p):
    '''
    assignment_statement : IDENT ASSIGN expression
    '''

    res = symbols.lookup(p[1])
    print('LOOKUP', res)


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
    while_statement : WHILE condition DO statement
    '''


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
    block_statement : BEGIN statement_list END
    '''

    # 手続きの終了
    if symbols.is_func:
        symbols.is_func = False
        res = symbols.delete()
        print('DELETE', res)


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


def p_expression(p):
    '''
    expression : term
               | PLUS term
               | MINUS term
               | expression PLUS term
               | expression MINUS term
    '''


def p_term(p):
    '''
    term : factor
         | term MULT factor
         | term DIV factor
    '''


def p_factor(p):
    '''
    factor : var_name
           | NUMBER
           | LPAREN expression RPAREN
    '''


def p_var_name(p):
    '''
    var_name : IDENT
    '''

    res = symbols.lookup(p[1])
    print('LOOKUP', res)


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
        res = symbols.insert(p[3], scope)
    else:
        res = symbols.insert(p[1], scope)
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

    # ファイルを開いて
    data = open(sys.argv[1]).read()
    # 解析を実行
    yacc.parse(data, lexer=lexer)
