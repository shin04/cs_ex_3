# -*- coding: utf-8 -*-

from enum import Enum


class CmpType(Enum):
    EQUAL = 0  # eq (==)
    NE = 1  # ne (!=)
    SGT = 2  # sgt (>，符号付き)
    SGE = 3  # sge (>=，符号付き)
    SLT = 4  # slt (<，符号付き)
    SLE = 5  # sle (<=，符号付き)

    def get_str(ctype):
        tab = {EQUAL: "eq", NE: "ne", SGT: "sgt", SGE: "sge", SLT: "slt", SLE: "sle"}
        return tab[ctype]


class LLVMCode(object):
    def __init__(self):
        pass


class LLVMCodeAlloca(LLVMCode):
    # localn variable
    def __init__(self, retval):
        super().__init__()
        self.retval = retval

    def __str__(self):
        return str(self.retval) + " = alloca i32, align 4"


class LLVMCodeGlobal(LLVMCode):
    # global variable
    def __init__(self, var_name):
        super().__init__()
        self.var_name = var_name

    def __str__(self):
        return str(self.var_name) + " = common global i32 0, align 4"


class LLVMCodeLoad(LLVMCode):
    def __init__(self, arg1, arg2):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return "{} = load i32, i32* {}, align 4".format(str(self.arg1), str(self.arg2))


class LLVMCodeStore(LLVMCode):
    def __init__(self, arg1, arg2):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return "store i32 {}, i32* {}, align 4".format(str(self.arg1), str(self.arg2))


class LLVMCodeBrUncond(LLVMCode):
    def __init__(self, arg1):
        super().__init__()
        self.arg1 = arg1

    def __str__(self):
        return "br label {}".format(str(self.arg1))


class LLVMCodeIcmp(LLVMCode):
    def __init__(self, cmptype, arg1, arg2, retval):
        super().__init__()
        self.cmptype = cmptype
        self.arg1 = arg1
        self.arg2 = arg2
        self.retval = retval

    def __str__(self):
        return "{} = icmp {} i32 {}, {}".format(
            str(self.retval), self.cmptype.get_str(), str(self.arg1), str(self.arg2),
        )


class LLVMCodeAdd(LLVMCode):
    def __init__(self, arg1, arg2, retval):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.retval = retval

    def __str__(self):
        return "{} = add nsw i32 {}, {}".format(self.retval, self.arg1, self.arg2)


class LLVMCodeSub(LLVMCode):
    def __init__(self, arg1, arg2, retval):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.retval = retval

    def __str__(self):
        return "{} = sub nsw i32 {}, {}".format(self.retval, self.arg1, self.arg2)


class LLVMCodeMul(LLVMCode):
    def __init__(self, arg1, arg2, retval):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.retval = retval

    def __str__(self):
        return "{} = mul nsw i32 {}, {}".format(self.retval, self.arg1, self.arg2)


class LLVMCodeSdiv(LLVMCode):
    def __init__(self, arg1, arg2, retval):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.retval = retval

    def __str__(self):
        return "{} = sdiv i32 {}, {}".format(self.retval, self.arg1, self.arg2)


class LLVMCodeRet(LLVMCode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "ret i32 0"
