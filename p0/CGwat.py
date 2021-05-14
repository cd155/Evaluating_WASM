
import nbimporter; nbimporter.options["only_defs"] = False
from SC import TIMES, DIV, MOD, AND, PLUS, MINUS, OR, EQ, NE, LT, GT, LE, GE, NOT, CARD, COMPLEMENT, UNION, INTERSECTION, ELEMENT, SUBSET, SUPERSET, SET,      mark
from ST import indent, Var, Const, Type, Proc, StdProc, Int, Bool, Array, Record, Set

def genProgStart():
    global curlev, memsize, asm
    curlev, memsize = 0, 0
    asm = ['(module',
           '(import "P0lib" "write" (func $write (param i32)))',
           '(import "P0lib" "writeln" (func $writeln))',
           '(import "P0lib" "read" (func $read (result i32)))']

def genBool(b: Bool):
    b.size = 1; return b

def genInt(i: Int):
    i.size = 4; return i

def genRec(r: Record):
    s = 0
    for f in r.fields:
        f.offset, s = s, s + f.tp.size
    r.size = s
    return r

def genArray(a: Array):
    a.size = a.length * a.base.size
    return a

def genSet(s: Set):
    if s.lower < 0 or s.lower + s.length > 32:
        mark('WASM: set too large')
    s.size = 4; return s

Global = 0; Stack = -1; MemInd = -2; MemAbs = -3

def genGlobalVars(sc, start):
    global memsize
    for i in range(start, len(sc)):
        if type(sc[i]) == Var:
            if sc[i].tp in (Int, Bool) or type(sc[i].tp) == Set:
                asm.append('(global $' + sc[i].name + ' (mut i32) i32.const 0)')
            elif type(sc[i].tp) in (Array, Record):
                sc[i].lev, sc[i].adr, memsize = MemAbs, memsize, memsize + sc[i].tp.size
            else: mark('WASM: type?')
    
def genLocalVars(sc, start):
    for i in range(start, len(sc)):
        if type(sc[i]) == Var:
            asm.append('(local $' + sc[i].name + ' i32)')
    asm.append('(local $0 i32)') # auxiliary local variable
    return sc[start:]

def loadItem(x):
    if type(x) == Var:
        if x.lev == Global: asm.append('global.get $' + x.name) # global Var
        elif x.lev == curlev: asm.append('local.get $' + x.name) # local Var
        elif x.lev == MemInd: asm.append('i32.load')
        elif x.lev == MemAbs:
            asm.append('i32.const ' + str(x.adr))
            if x.tp in {Int, Bool}: asm.append('i32.load')
        elif x.lev != Stack: mark('WASM: var level!') # already on stack if lev == Stack
    else: asm.append('i32.const ' + str(x.val))

def genVar(x):
    if Global < x.lev < curlev: mark('WASM: level!')
    y = Var(x.tp); y.lev, y.name = x.lev, x.name
    if x.lev == MemAbs: y.adr = x.adr
    return y

def genConst(x):
    # x is Const
    x.lev = None # constants are either not stored or on stack, lev == Stack
    return x

def genUnaryOp(op, x):
    loadItem(x)
    if op == MINUS:
        asm.append('i32.const -1')
        asm.append('i32.mul')
        x = Var(Int); x.lev = Stack
    elif op == CARD:
        asm.append('i32.popcnt')
        x = Var(Int); x.lev = Stack
    elif op == COMPLEMENT:
        u = (1 << x.tp.length) - 1 # x.tp.length 1's
        u = u << x.tp.lower # universe of base type
        asm.append('i32.const ' + hex(u))
        asm.append('i32.xor')
        x = Var(x.tp); x.lev = Stack
    elif op == SET:
        asm.append('local.set $0')
        asm.append('i32.const 1')
        asm.append('local.get $0')
        asm.append('i32.shl')
        x = Var(Set(0, 32)); x.lev = Stack
    elif op == NOT:
        asm.append('i32.eqz')
        x = Var(Bool); x.lev = Stack
    elif op == AND:
        asm.append('if (result i32)')
        x = Var(Bool); x.lev = Stack
    elif op == OR:
        asm.append('if (result i32)')
        asm.append('i32.const 1')
        asm.append('else')
        x = Var(Bool); x.lev = Stack
    elif op == ELEMENT:
        asm.append('local.set $0')
        asm.append('i32.const 1')
        asm.append('local.get $0')
        asm.append('i32.shl')
        x = Var(Int); x.lev = Stack
    elif op in {SUBSET, SUPERSET}:
        asm.append('local.tee $0')
        asm.append('local.get $0')
        x.lev = Stack
    else: mark('WASM: unary operator?')
    return x


def genBinaryOp(op, x, y):
    if op in (PLUS, MINUS, TIMES, DIV, MOD):
        loadItem(x); loadItem(y)
        asm.append('i32.add' if op == PLUS else                    'i32.sub' if op == MINUS else                    'i32.mul' if op == TIMES else                    'i32.div_s' if op == DIV else                    'i32.rem_s' if op == MOD else '?')
        x = Var(Int); x.lev = Stack
    elif op in {UNION, INTERSECTION}:
        loadItem(x); loadItem(y)
        asm.append('i32.or' if op == UNION else                    'i32.and' if op == INTERSECTION else '?')
        x = Var(x.tp); x.lev = Stack
    elif op == AND:
        loadItem(y) # x is already on the stack
        asm.append('else')
        asm.append('i32.const 0')
        asm.append('end')
        x = Var(Bool); x.lev = Stack
    elif op == OR:
        loadItem(y) # x is already on the stack
        asm.append('end')
        x = Var(Bool); x.lev = Stack
    else: mark('WASM: binary operator?')
    return x

def genRelation(op, x, y):
    loadItem(x); loadItem(y)
    asm.extend(['i32.eq'] if op == EQ else                ['i32.ne'] if op == NE else                ['i32.lt_s'] if op ==  LT else                ['i32.gt_s'] if op == GT else                ['i32.le_s'] if op == LE else                ['i32.ge_s'] if op == GE else                ['i32.and'] if op == ELEMENT else                ['i32.and', 'i32.eq'] if op == SUBSET else                ['i32.or', 'i32.eq'] if op == SUPERSET else '?')
    x = Var(Bool); x.lev = Stack
    return x

def genIndex(x, y):
    # x[y], assuming x.tp is Array and x is global Var, local Var
    # and y is Const, local Var, global Var, stack Var
    if x.lev == MemAbs and type(y) == Const: 
        x.adr += (y.val - x.tp.lower) * x.tp.base.size
        x.tp = x.tp.base
    else:
        loadItem(y)
        if x.tp.lower != 0:
            asm.append('i32.const ' + str(x.tp.lower))
            asm.append('i32.sub')
        asm.append('i32.const ' + str(x.tp.base.size))
        asm.append('i32.mul')
        if x.lev > 0: asm.append('local.get $' + x.name)
        elif x.lev == MemAbs: asm.append('i32.const ' + str(x.adr))
        asm.append('i32.add')
        x = Var(x.tp.base)
        if x.tp in (Int, Bool) or type(x.tp) == Set: x.lev = MemInd
        else: x.lev = Stack
    return x

def genSelect(x, f):
    # x.f, assuming x.tp is Record, f is Field, and x.lev is Stack, MemInd or is > 0
    if x.lev == MemAbs: x.adr += f.offset
    elif x.lev == Stack:
        asm.append('i32.const ' + str(f.offset))
        asm.append('i32.add')
    elif x.lev > 0:
        asm.append('local.get $' + x.name) # parameter or local reference
        asm.append('i32.const ' + str(f.offset))
        asm.append('i32.add')
        x.lev = Stack
    else: mark('WASM: select?')
    x.tp = f.tp
    return x

def genLeftAssign(x):
    if x.lev == MemAbs: asm.append('i32.const ' + str(x.adr))
    elif x.lev > 0 and type(x.tp) in (Array, Record):
        asm.append('local.get $' + x.name)
    return x

def genRightAssign(x):
    loadItem(x); y = Var(x.tp); y.lev = Stack; return y


def genAssign(x, y):
    loadItem(y)
    if x.lev == Global: asm.append('global.set $' + x.name)
    elif x.lev > 0:
        if type(x.tp) in (Array, Record):
            asm.append('i32.const ' + str(x.tp.size))
            asm.append('memory.copy')
        else: asm.append('local.set $' + x.name)
    else:
        if type(x.tp) in (Array, Record):
            asm.append('i32.const ' + str(x.tp.size))
            asm.append('memory.copy')
        else: asm.append('i32.store')

def genProgEntry(ident):
    global curlev
    curlev = curlev + 1
    asm.append('(global $_memsize (mut i32) i32.const ' + str(memsize) + ')')
    asm.append('(func $program')

def genProgExit(x):
    global curlev
    curlev = curlev - 1
    asm.append('(memory ' + str(memsize // 2** 16 + 1) + ')\n(start $program)\n)')
    return '\n'.join(l for l in asm)

def genProcStart(ident, fp, rp):
    global curlev
    if curlev > 0: mark('WASM: no nested procedures')
    curlev = curlev + 1
    asm.append('(func $' + ident + ' ' +
               ' '.join('(param $' + e.name + ' i32)' for e in fp) + ' ' + 
               ' '.join('(result i32)' for e in rp) +
               ('\n' if len(rp) > 0 else '') +
               '\n'.join('(local $' + e.name + ' i32)' for e in rp))
    return rp

def genProcEntry(ident, para, local):
    pl = (para if para else []) + local
    if any(type(l) == Var and type(l.tp) in (Array, Record) for l in pl):
        asm.append('(local $_mp i32)')
        asm.append('global.get $_memsize')
        asm.append('local.set $_mp')
    for l in pl:
        if type(l) == Var and type(l.tp) in (Array, Record):
            asm.append('global.get $_memsize')
            asm.append('local.tee $' + l.name)
            asm.append('i32.const ' + str(l.tp.size))
            asm.append('i32.add')
            asm.append('global.set $_memsize')

def genProcExit(x, para, local):
    global curlev
    curlev = curlev - 1
    pl = (para if para else []) + local
    if any(type(l) == Var and type(l.tp) in (Array, Record) for l in pl):
        asm.append('local.get $_mp')
        asm.append('global.set $_memsize')
    if para: asm.append('\n'.join('local.get $' + e.name for e in para))
    asm.append(')')

def genActualPara(ap, fp, n):
    if ap.tp in {Int, Bool} or type(ap.tp) == Set: loadItem(ap)
    else: # a.tp is Array, Record
        if ap.lev > 0: asm.append('local.get $' + ap.name)
        elif ap.lev == MemAbs: asm.append('i32.const ' + str(ap.adr))
        elif ap.lev != Stack: mark('WASM: actual parameter?')

def genCall(rp, pr, ap): # result (or None), procedure, actual parameters
    asm.append('call $' + pr.name)
    for r in reversed(rp): y = Var(Int); y.lev = Stack; genAssign(r, y)

def genRead(x):
    asm.append('call $read')
    y = Var(Int); y.lev = Stack; genAssign(x, y)

def genWrite(x):
    asm.append('call $write')

def genWriteln():
    asm.append('call $writeln')

def genSeq(x, y):
    pass

def genThen(x):
    loadItem(x)
    asm.append('if')
    return x

def genIfThen(x, y):
    asm.append('end')

def genElse(x, y):
    asm.append('else')

def genIfElse(x, y, z):
    asm.append('end')

def genWhile():
    asm.append('loop')

def genDo(x):
    loadItem(x)
    asm.append('if')
    return x

def genWhileDo(t, x, y):
    asm.append('br 1')
    asm.append('end')
    asm.append('end')
