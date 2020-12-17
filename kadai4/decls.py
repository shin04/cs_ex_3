# -*- coding: utf-8 -*-

from enum import Enum

from symtab import Scope


class Fundecl(object):
    def __init__(self, name):
        self.name = name
        self.codes = []
        self.cntr = 1
        self.rettype = "void"

    def get_register(self):
        t = self.cntr
        self.cntr += 1
        return t

    def print(self, fp):
        if self.name != "":
            print("define {} @{}(){{".format(self.rettype, self.name), file=fp)
            for l in self.codes:
                print("  {}".format(l), file=fp)
            print("}", file=fp)
        else:
            for l in self.codes:
                print("{}".format(l), file=fp)


class Factor(object):
    def __init__(self, vtype, vname=None, val=None):
        self.type = vtype
        self.name = vname
        self.val = val

    def __str__(self):
        if self.type == Scope.GLOBAL:
            return "@{}".format(self.name)
        elif self.type == Scope.LOCAL:
            return "%{}".format(self.val)
        elif self.type == Scope.CONSTANT:
            return "{}".format(self.val)
        elif self.type == Scope.FUNC:
            return "@{}()".format(self.name)
