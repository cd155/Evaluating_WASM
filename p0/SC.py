
TIMES = 1; DIV = 2; MOD = 3; AND = 4; PLUS = 5; MINUS = 6
OR = 7; EQ = 8; NE = 9; LT = 10; GT = 11; LE = 12; GE = 13
PERIOD = 14; COMMA = 15; COLON = 16; NOT = 17; LPAREN = 18
RPAREN = 19; LBRAK = 20; RBRAK = 21; LARROW = 22; RARROW = 23
LBRACE = 24; RBRACE = 25; CARD = 26; COMPLEMENT = 27; UNION = 28
INTERSECTION = 29; ELEMENT = 30; SUBSET = 31; SUPERSET = 32
DOTDOT = 33; THEN = 34; DO = 35; BECOMES = 36; NUMBER = 37
IDENT = 38; SEMICOLON = 39; ELSE = 40; IF = 41; WHILE = 42
CONST = 43; TYPE = 44; VAR = 45; SET = 46; PROCEDURE = 47
PROGRAM = 48; INDENT = 49; DEDENT = 50; EOF = 51; FUNC = 52

def init(src):
    global line, lastline, pos, lastpos
    global ch, sym, val, source, index, indents
    line, lastline = 0, 1
    pos, lastpos = 1, 1
    ch, sym, val, source, index = '\n', None, None, src, 0
    indents = [1]; getChar(); getSym()

def getChar():
    global line, lastline, pos, lastpos, ch, index
    if index == len(source): ch, index, pos = chr(0), index + 1, 1
    else:
        lastpos = pos
        if ch == '\n':
            pos, line = 1, line + 1
        else:
            lastline, pos = line, pos + 1
        ch, index = source[index], index + 1

def mark(msg):
    raise Exception('line ' + str(lastline) + ' pos ' + str(lastpos) + ' ' + msg)

def number():
    global sym, val
    sym, val = NUMBER, 0
    while '0' <= ch <= '9':
        val = 10 * val + int(ch)
        getChar()
    if val >= 2**31: mark('number too large')

KEYWORDS = {'div': DIV, 'mod': MOD, 'and': AND, 'or': OR, 'then': THEN, 'do': DO,
     'else': ELSE, 'if': IF, 'while': WHILE, 'const': CONST, 'type': TYPE,
     'var': VAR, 'set': SET, 'procedure': PROCEDURE, 'program': PROGRAM}

def identKW():
    global sym, val
    start = index - 1
    while ('A' <= ch <= 'Z') or ('a' <= ch <= 'z') or ('0' <= ch <= '9'): getChar()
    val = source[start : index - 1]
    sym = KEYWORDS[val] if val in KEYWORDS else IDENT

def comment():
    if ch == '/': getChar()
    else: mark('// expected')
    while chr(0) != ch != '\n': getChar()

def getSym():
    global sym, indents, newline
    if pos < indents[0]:
        indents = indents[1:]; sym = DEDENT
    else:
        while ch in ' /':
            if ch == ' ': getChar() # skip blanks between symbols
            else: comment()
        if ch == '\n': # possibly INDENT, DEDENT
            while ch == '\n': # skip blank lines
                getChar()
                while ch in ' /':
                    if ch == ' ': getChar() # skip indentation
                    else: comment()
            if pos < indents[0]: sym, indents = DEDENT, indents[1:]; return
            elif pos > indents[0]: sym, indents = INDENT, [pos] + indents; return
        newline = pos == indents[0]
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z': identKW()
        elif '0' <= ch <= '9': number()
        elif ch == '×': getChar(); sym = TIMES
        elif ch == '+': getChar(); sym = PLUS
        elif ch == '-': getChar(); sym = MINUS
        elif ch == '=': getChar(); sym = EQ
        elif ch == '≠': getChar(); sym = NE
        elif ch == '<': getChar(); sym = LT
        elif ch == '≤': getChar(); sym = LE
        elif ch == '>': getChar(); sym = GT
        elif ch == '≥': getChar(); sym = GE
        elif ch == ';': getChar(); sym = SEMICOLON
        elif ch == ',': getChar(); sym = COMMA
        elif ch == ':':
            getChar()
            if ch == '=': getChar(); sym = BECOMES
            else: sym = COLON
        elif ch == '.':
            getChar();
            if ch == '.': getChar(); sym = DOTDOT
            else: sym = PERIOD
        elif ch == '¬': getChar(); sym = NOT
        elif ch == '(': getChar(); sym = LPAREN
        elif ch == ')': getChar(); sym = RPAREN
        elif ch == '[': getChar(); sym = LBRAK
        elif ch == ']': getChar(); sym = RBRAK
        elif ch == '←': getChar(); sym = LARROW
        elif ch == '→': getChar(); sym = RARROW
        elif ch == '{': getChar(); sym = LBRACE
        elif ch == '}': getChar(); sym = RBRACE
        elif ch == '#': getChar(); sym = CARD
        elif ch == '∁': getChar(); sym = COMPLEMENT
        elif ch == '∪': getChar(); sym = UNION
        elif ch == '∩': getChar(); sym = INTERSECTION
        elif ch == '∈': getChar(); sym = ELEMENT
        elif ch == '⊆': getChar(); sym = SUBSET
        elif ch == '⊇': getChar(); sym = SUPERSET
        elif ch == chr(0): sym = EOF
        else: mark('illegal character')
