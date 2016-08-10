#!/usr/bin/env python3

"""Experiment with parsing USP data model paths and expressions."""

# XXX add logging controls

class PathError(Exception): pass
class LexerError(PathError): pass
class EndOfInput(LexerError): pass
class ParserError(PathError): pass

class PathLexer:
    """Lexer (tokenizer) that returns tokens from a USP path expression.
    """

    # operators (and punctuation)
    _operators = ["=", ".", "+", "*", "[", ",", "]", "{", "}", "()", "&&",
                  "==", "!=", "<", "<=", ">", ">=", "::"]

    # the above sorted by length (longest to shortest)
    _operators = sorted(_operators, key=len, reverse=True)

    # first characters of the above; used for determining whether the next
    # token is an operator (or punctuation)
    _operator_starts = set([oper[0] for oper in _operators])

    # XXX support options, e.g. no-wildcard
    def __init__(self, text):
        # USP path to process
        self._text = text

        # position of next character to scan
        self._start = 0

        # position of character after last character of current token
        # set _start to _end to advance over current token
        self._end = 0

        # type and value of current token; valid when _end > _start
        self._current = ("", None)

        # the rest of the text starting at the current token
        # XXX should store this as a cached _start pointer
        self._rest = text

    def next(self):
        """Return the current token type and value, and advance to the next
        token."""

        current = self.peek()
        self.advance()
        return current

    def peek(self):
        """Return the current token type and value.
        """

        if self._end <= self._start:
            self._peek()

        #print("peek", self._current)
        return self._current

    def advance(self):
        """Advance to the next token.
        """
        
        self._start = self._end

    def rest(self):
        """The rest of the text starting at the current token.
        """

        return self._rest

    # XXX method names are confusing
    def _peek(self):
        """Determine the next token type and value, regardless of whether the
        current token is known. Sets _rest and _current.
        """
        
        # skip leading white space
        # XXX maybe shouldn't permit any?
        #while self._text[self._start:self._start+1].isspace():
        #    self._start += 1

        # remember the rest of the text starting at the next token
        self._rest = self._text[self._start:]
        
        ptr = self._start
        tlen = len(self._text)
        char = self._text[ptr:ptr+1]

        # anything left in the input string?
        # XXX it really would be better to handle this as a token type
        if ptr >= tlen:
            raise EndOfInput

        # operator (longest first)
        elif char in self._operator_starts:
            found = False
            for oper in self._operators:
                token = self._text[ptr:ptr+len(oper)]
                if token == oper:
                    self._end = ptr + len(oper)
                    self._current = (oper, oper)
                    found = True
                    break
            if not found:
                raise LexerError("Expected operator %s at '%s'" %
                                 (self._operators, self._text[self._start:]))

        # quoted string literal
        # XXX this allows single quote within double quoted string and vice
        #     versa, but doesn't allow a string to contain both single and
        #     double quotes; could allow them to be backslash (?) escaped, or
        #     else use percent encoding
        elif char in ['"', "'"]:
            ptr += 1
            literal = ""
            while ptr < tlen and self._text[ptr] != char:
                literal += self._text[ptr]
                ptr += 1
            if ptr >= tlen:
                raise LexerError("Unterminated string at '%s'" %
                                 self._text[self._start:])
            self._end = ptr + 1
            self._current = ("literal", literal)

        # number
        elif char == "-" or char.isdigit():
            if char != "-":
                negative = False
            else:
                negative = True
                if ptr >= tlen:
                    raise LexerError("Unterminated number at '%s'" %
                                     self._text[self._start:])
                ptr += 1
            number = 0
            while ptr < tlen and self._text[ptr].isdigit():
                number = 10 * number + int(self._text[ptr])
                ptr += 1
            self._end = ptr
            if negative:
                number = -number
            self._current = ("number", number)

        # name (identifier)
        elif char.isidentifier():
            name = ""
            while ptr < tlen and (self._text[ptr].isidentifier() or
                                  self._text[ptr].isdigit()):
                name += self._text[ptr]
                ptr += 1
            self._end = ptr
            self._current = ("name", name)

        # otherwise invalid
        else:
            raise LexerError("Invalid token at '%s'" %
                             self._text[self._start:])

class PathParser:
    def __init__(self, lexer):
        self._lexer = lexer

    def parse(self):
        return self._parse_path()

    def _parse_path(self):
        """path : comps expr?
        """

        comps = self._parse_comps()

        expr = None
        try:
            expr = self._parse_expr()
        except EndOfInput:
            pass

        return (comps, expr)
    
    def _parse_comps(self):
        """comps : comp ( '.' comp )* '.'?
        """

        comps = []

        try:
            comp = self._parse_comp()
            comps.append(comp)
            
            (type, token) = self._lexer.peek()
            while type == ".":
                self._lexer.advance()
                #comps.append(("namesep", "."))
                (type, token) = self._lexer.peek()
                if type == "::":
                    break
                comp = self._parse_comp()
                comps.append(comp)
                (type, token) = self._lexer.peek()
        except EndOfInput:
            pass

        return comps
            
    def _parse_comp(self):
        """comp : namemod
                | inst
        """
        
        (type, token) = self._lexer.peek()
        if type == "name":
            namemod = self._parse_namemod()
            comp = ("namemod", namemod)
        else:
            inst = self._parse_inst()
            comp = ("inst", inst)

        #print("comp", comp)
        return comp

    # XXX would be more consistent to use "wildcard" rather than '*'
    def _parse_inst(self):
        """inst : number
                | keyref
                | exprvar
                | '*'
        """
        
        (type, token) = self._lexer.peek()
        if type == "number":
            self._lexer.advance()
            if token <= 0:
                raise ParserError("Invalid instance number at %s" %
                                  self._lexer.rest())
            inst = ("number", token)
            
        elif type == "[":
            keyref = self._parse_keyref()
            inst = ("keyref", keyref)
            
        elif type == "{":
            exprvar = self._parse_exprvar()
            inst = ("exprvar", exprvar)
            
        elif type == "*":
            self._lexer.advance()
            inst = ("wildcard", token)
            
        else:
            raise ParserError("Invalid instance at %s" % self._lexer.rest())

        #print("  inst", inst)
        return inst

    def _parse_keyref(self):
        """keyref : '[' keyexpr ( ',' keyexpr )* ']'
        """

        keyexprs = []

        self._parse_punct("[")
        
        keyexpr = self._parse_keyexpr()
        keyexprs.append(keyexpr)
        
        (type, token) = self._lexer.peek()
        while type == ",":
            self._lexer.advance()
            keyexpr = self._parse_keyexpr()
            keyexprs.append(keyexpr)
            (type, token) = self._lexer.peek()

        self._parse_punct("]")
        
        return keyexprs[0] if len(keyexprs) == 1 else keyexprs

    def _parse_exprvar(self):
        """exprvar : '{' name '}'
        """

        self._parse_punct("{")
        name = self._parse_name()
        self._parse_punct("}")
        
        return name

    # XXX note that this uses "=" rather than "=="
    def _parse_keyexpr(self):
        """keyexpr : relpath '=' value
        """

        relpath = self._parse_relpath()
        oper = self._parse_punct("=")
        value = self._parse_value()

        return (relpath, oper, value)
        
    def _parse_relpath(self):
        """relpath : namemod ( '.' namemod )*
        """
        
        namemods = [self._parse_namemod()]

        (type, token) = self._lexer.peek()
        while type == ".":
            self._lexer.advance()
            namemod = self._parse_namemod()
            namemods.append(namemod)
            (type, token) = self._lexer.peek()

        #print("namemods", namemods)
        return namemods[0] if len(namemods) == 1 else namemods

    def _parse_expr(self):
        """expr : '::' exprbody
        """

        self._parse_punct("::")
        exprbody = self._parse_exprbody()

        return exprbody

    def _parse_exprbody(self):
        """exprbody : '{' exprcomp ( '&&' exprcomp )* '}'
        """

        exprcomps = []

        self._parse_punct("{")
        
        exprcomp = self._parse_exprcomp()
        exprcomps.append(exprcomp)
        
        (type, token) = self._lexer.peek()
        while type == "&&":
            self._lexer.advance()
            exprcomp = self._parse_exprcomp()
            exprcomps.append(exprcomp)
            (type, token) = self._lexer.peek()

        self._parse_punct("}")
        
        return exprcomps[0] if len(exprcomps) == 1 else exprcomps

    def _parse_exprcomp(self):
        """exprcomp : relpath oper value
        """

        relpath = self._parse_relpath()
        oper = self._parse_oper()
        value = self._parse_value()

        return (relpath, oper, value)

    def _parse_namemod(self):
        """namemod : name '+'? '()'?         
        """

        namemod = [self._parse_name()]
        
        (type, token) = self._lexer.peek()
        if token == "+":
            self._lexer.advance()
            namemod.append('deref')
        (type, token) = self._lexer.peek()
        if token == "()":
            self._lexer.advance()
            namemod.append('command')
        
        return namemod[0] if len(namemod) == 1 else tuple(namemod)
    
    def _parse_name(self):
        """name : name                
        """
        
        return self._parse_util("name", ["name"])
    
    def _parse_oper(self):
        """oper : '=='
                | '!='
                | '<'
                | '>'
                | '<='
                | '>='
        """

        return self._parse_util("operator", ["==", "!=", "<", ">", "<=", ">="])

    def _parse_value(self):
        """value : literal
                 | number
        """

        return self._parse_util("value", ["literal", "number"])

    def _parse_punct(self, punct):
        """token : punct
        """

        return self._parse_util("'" + punct + "'", [punct])

    def _parse_util(self, label, types):
        """token : types
        """
        
        (type, value) = self._lexer.peek()
        if type not in types:
            types_str = " (" + ",".join(types) + ")" \
                        if len(types) > 1 else ""
            raise ParserError("Expected %s%s at '%s'" %
                              (label, types_str, self._lexer.rest()))
        
        self._lexer.advance()
        return value

model = {
    "Device": {
        "IP": {
            "Interface": {
                "{i}": None,
                1: {
                    "Name": "lan",
                    "Enable": 0
                },
                2: {
                    "Name": "wan",
                    "Enable": 1
                },
                3: {
                    "Name": "ppp",
                    "Enable": 1
                },
            },
        },
    },
}

# XXX create "proper" main program
import sys
for path in sys.argv[1:]:
    print("path", path)
    parser = PathParser(PathLexer(path))
    try:
        (comps, expr) = parser.parse()
        for (i, comp) in enumerate(comps):
            print("  comp", comp)
        print("  expr", expr)
    except PathError as e:
        sys.stderr.write("# %s: %s\n" % (e.__class__.__name__, e))
sys.exit(0)

path = 'Device.IP.Interface.[Name="wan"][Enable].Enable'

print(path)
#print(comps)
#sys.exit(0)

# XXX this is just proof of concept; need re-writing as understandble
#     recursive algorithm
text = ''
dict = model
for comp in comps:
    print(comp)
    (type, value) = comp
    if type == "name":
        if value not in dict:
            print(value, "not in", list(dict.keys()))
        else:
            text += value + "."
            dict = dict[value]
    elif type == "inst":
        (type, value) = value
        if "{i}" not in dict:
            print(" ", "not a table")
            break
        if type == "number":
            instnum = value
            if instnum not in dict:
                print(" ", "not found")
                break
            text += str(instnum) + "."
            dict = dict[instnum]
        elif type == "wildcard":
            instnums = list(set(dict.keys()) - set(["{i}"]))
            print(" ", "expands to", instnums)
            text += str(instnums) + "."
            dict = dict[instnums[0]]
        elif type == "exprs":
            instnums = list(set(dict.keys()) - set(["{i}"]))
            exprs = value
            for (type, value) in exprs:
                if type == "simple":
                    print(" ", value)
                    (name, oper, value) = value
                    oper = "==" if oper == "=" else oper
                    matches = []
                    for instnum in instnums:
                        nameval = dict[instnum][name]
                        # XXX shouldn't use string comparison?
                        expr = '"%s" %s "%s"' % (nameval, oper, value)
                        result = eval(expr)
                        print("   ", instnum, expr, "->", result)
                        if result:
                            matches.append(instnum)
                    if not matches:
                        break
                    print("   ", "matches for", matches)
                else:
                    print(" ", type, "not supported")
                    break
                instnums = matches
            if not matches:
                print("   ", "no matches")
                break
            text += str(matches[0]) + "."
            dict = dict[matches[0]]
        else:
            print(" ", type, "not supported")
            break
print(text)
