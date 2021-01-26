# -*- coding: utf-8 -*-

from enum import Enum


class Scope(Enum):
    LOCAL = 0
    GLOBAL = 1
    FUNC = 2
    CONSTANT = 3


class SymbolTable(object):
    def __init__(self):
        # symbols = [[var_name, var_address, var_type]]
        self.symbols = []
        self.is_func = False
        self.is_args = False
        # self.is_block = False
        self.block_count = 0
        self.is_else_block = False

    def insert(self, token: str, token_type: Scope, address=0) -> list:
        symbol = [token, address, token_type]
        self.symbols.append(symbol)

        return self.symbols

    def countup(self, token: str) -> int:
        count = 0
        for symbol in self.symbols:
            if symbol[0] == token:
                count += 1
        return count

    def lookup(self, token: str, scope: Scope = None) -> list:
        res = []
        for symbol in self.symbols:
            if symbol[0] == token:
                if scope != None:
                    if scope == symbol[2]:
                        res = symbol
                        break
                else:
                    res = symbol
                    break

        return res

    def delete(self) -> list:
        new_symbol = []
        for symbol in self.symbols:
            if symbol[2] != Scope.LOCAL:
                new_symbol.append(symbol)
        self.symbols = new_symbol

        return self.symbols
