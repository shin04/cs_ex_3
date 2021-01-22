# -*- coding: utf-8 -*-

from enum import Enum

from symtab import Scope


class Fundecl(object):
    def __init__(self, name):
        self.name = name
        self.arglist = []  # arg type
        self.codes = []
        self.cntr = 1
        self.rettype = "void"
        self.retval = Factor(Scope.LOCAL, val=0)
        self.use_read = ""
        self.use_write = ""

    def get_register(self):
        t = self.cntr
        self.cntr += 1
        return t

    def print_arglist(self):
        res = ''
        for i, arg in enumerate(self.arglist):
            if i > 0:
                res += ', '
            res += arg

        return res

    def print(self, fp):
        if self.name != "":
            print("define {} @{}({}){{".format(self.rettype, self.name, self.print_arglist()), file=fp)
            for l in self.codes:
                print("  {}".format(l), file=fp)
            print("}", file=fp)

            if self.use_read != "":
                print(self.use_read, file=fp)
            if self.use_write != "":
                print(self.use_write, file=fp)
        else:
            for l in self.codes:
                print("{}".format(l), file=fp)


class Factor(object):
    def __init__(self, vtype, vname=None, val=None, ret=False):
        self.type = vtype
        self.name = vname
        self.val = val
        self.ret = ret

    def __str__(self):
        if self.type == Scope.GLOBAL:
            return "@{}".format(self.name)
        elif self.type == Scope.LOCAL:
            return "%{}".format(self.val)
        elif self.type == Scope.CONSTANT:
            return "{}".format(self.val)
        elif self.type == Scope.FUNC:
            return '@{}'.format(self.name)
