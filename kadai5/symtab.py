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

    def insert(self, token: str, token_type: Scope) -> list:
        symbol = [token, 0, token_type]
        self.symbols.append(symbol)

        return self.symbols

    def lookup(self, token: str) -> list:
        res = []
        for symbol in self.symbols:
            if symbol[0] == token:
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
