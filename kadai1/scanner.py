# -*- coding: utf-8 -*-

import sys

import ply.lex as lex
import ply.yacc as yacc

tokens = ('IDENT', 'NUMBER', 'BEGIN', ・・・, 'ASSIGN')

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

t_PLUS = r'\+'
t_MINUS = '-'
・・・
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
    print("不正な文字「", t.value[0], "」")
    t.lexer.skip(1)


if __name__ == "__main__":
    lexer = lex.lex(debug=0)

    data = open(sys.argv[1]).read()
    lexer.input(data)

    while 1:
        tok = lexer.token()
        if not tok:
            break
        print(tok.lineno, tok.type, tok.value)
