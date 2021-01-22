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
        tab = {0: "eq", 1: "ne", 2: "sgt", 3: "sge", 4: "slt", 5: "sle"}
        return tab[ctype.value]


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


class LLVMCodeBrCond(LLVMCode):
    def __init__(self, arg1, arg2, arg3):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def __str__(self):
        return "br i1 {}, label {}, label {}".format(
            str(self.arg1), str(self.arg2), str(self.arg3)
        )


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
    def __init__(self, rtype='i32', val=0):
        super().__init__()
        self.rtype = rtype
        self.val = val

    def __str__(self):
        if self.rtype == 'void':
            return "ret {}".format(self.rtype)
        elif self.rtype == 'main':
            return "ret i32 0"
        else:
            return "ret {} {}".format(self.rtype, self.val)


class LLVMCodeLabel(LLVMCode):
    def __init__(self, arg1):
        super().__init__()
        self.arg1 = arg1.val

    def __str__(self):
        return '{}:'.format(self.arg1)


class LLVMCodeProcCall(LLVMCode):
    def __init__(self, rtype, name, args=[], reg=None):
        super().__init__()
        self.rtype = rtype
        self.name = name
        self.args = args
        self.reg = reg

    def __str__(self):
        args_str = ''
        for i, arg in enumerate(self.args):
            if i > 0:
                args_str += ', '
            args_str += arg[1] + ' ' + arg[0]

        if self.reg == None:
            return 'call {} {}({})'.format(self.rtype, self.name, args_str)
        else:
            return '{} = call {} {}({})'.format(self.reg, self.rtype, self.name, args_str)


class LLVMCodeOutProcCall(LLVMCode):
    def __init__(self, retval, proc_type, proc, var, var_type):
        self.retval = retval
        self.proc_type = proc_type
        self.proc = proc
        self.var_type = var_type
        self.var = var

    def __str__(self):
        return '{} = call {} (i8*, ...) @{}(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), {} {})'.format(self.retval, self.proc_type, self.proc, self.var, self.var_type)


class LLVMCodeDeclare(LLVMCode):
    def __init__(self, proc_type, proc):
        self.proc_type = proc_type
        self.proc = proc

    def __str__(self):
        return 'declare {} @{}(i8*, ...)'.format(self.proc_type, self.proc)
