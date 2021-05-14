
import nbimporter, textwrap
nbimporter.options["only_defs"] = False
from SC import mark

def indent(n):
    return textwrap.indent(str(n), '  ')

class Var:
    def __init__(self, tp):
        self.tp = tp
    def __str__(self):
        return 'Var(name = ' + str(getattr(self, 'name', '')) + ', lev = ' + str(getattr(self, 'lev', '')) + ', tp = ' + str(self.tp) + ')'
    def __eq__(self, other):
        return self.reg == other.reg and self.adr == other.adr
    def __hash__(self):
        return hash(str(self))

class Ref:
    def __init__(self, tp):
        self.tp = tp
    def __str__(self):
        return 'Ref(name = ' + str(getattr(self, 'name', '')) + ', lev = ' + str(getattr(self, 'lev', '')) + ', tp = ' + str(self.tp) + ')'

class Res:
    def __init__(self, tp):
        self.tp = tp
    def __str__(self):
        return 'Res(name = ' + str(getattr(self, 'name', '')) + ', lev = ' + str(getattr(self, 'lev', '')) + ', tp = ' + str(self.tp) + ')'

class Const:
    def __init__(self, tp, val):
        self.tp, self.val = tp, val
    def __str__(self):
        return 'Const(name = ' + str(getattr(self, 'name', '')) + ', tp = ' + str(self.tp) + ', val = ' + str(self.val) + ')'
    def __eq__(self, other):
        return self.val == other.val
    def __hash__(self):
        return hash(str(self))

class Type:
    def __init__(self, tp):
        self.tp, self.val = None, tp
    def __str__(self):
        return 'Type(name = ' + str(getattr(self, 'name', '')) + ', val = ' + str(self.val) + ')'

class Proc:
    def __init__(self, par, res):
        self.tp, self.par, self.res = None, par, res
    def __str__(self):
        return 'Proc(name = ' + self.name + ', lev = ' + str(self.lev) + ', par = [' + ', '.join(str(s) for s in self.par) + ']' +                ', res = [' + ', '.join(str(s) for s in self.res) + '])'

class StdProc:
    def __init__(self, par, res):
        self.tp, self.par, self.res = None, par, res
    def __str__(self):
        return 'StdProc(name = ' + self.name + ', lev = ' + str(self.lev) + ', par = [' + ', '.join(str(s) for s in self.par) + ']' +                ', res = [' + ', '.join(str(s) for s in self.res) + '])'

class Int: pass

class Bool: pass

class Record:
    def __init__(self, fields):
        self.fields = fields
    def __str__(self):
        return 'Record(fields = [' + ', '.join(str(f) for f in self.fields) + '])'

class Array:
    def __init__(self, base, lower, length):
        self.base, self.lower, self.length = base, lower, length
    def __str__(self):
        return 'Array(lower = ' + str(self.lower) + ', length = ' + str(self.length) + ', base = ' + str(self.base) + ')'

class Set:
    def __init__(self, lower, length):
        self.lower, self.length = lower, length
    def __str__(self):
        return 'Set(lower = ' + str(self.lower) + ', length = ' + str(self.length) + ')'

def init():
    global symTab
    symTab = [[]]

def printSymTab():
    print('symbol table:')
    for l in symTab:
        for e in l: print(e)
        print()

def newDecl(name, entry):
    top, entry.lev, entry.name = symTab[0], len(symTab) - 1, name
    for e in top:
        if e.name == name:
            mark("multiple definition of " + str(name)); return
    top.append(entry)

def find(name):
    for l in symTab:
        for e in l:
            if name == e.name: return e
    mark('undefined identifier ' + name)
    return Const(None, 0)

def openScope():
    symTab.insert(0, [])

def topScope():
    return symTab[0]

def closeScope():
    symTab.pop(0)
