#!/usr/bin/env python3

"""Experiment with parsing USP data model paths."""

# XXX add logging controls

class PathError(Exception): pass
class LexerError(PathError): pass
class EndOfInput(LexerError): pass
class ParserError(PathError): pass

class PathLexer:
    """Lexer (tokenizer) that returns tokens from a USP path expression.
    """

    # operators (and punctuation)
    _operators = [".", "*", "[", "]", "=", "!=", "<", "<=", ">", ">="]

    # the above sorted by length (shortest to longest)
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
        while self._text[self._start:self._start+1].isspace():
            self._start += 1

        # remember the rest of the text starting at the next token
        self._rest = self._text[self._start:]
        
        ptr = self._start
        tlen = len(self._text)
        char = self._text[ptr:ptr+1]

        # anything left in the input string?
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
                raise LexerError("Expected operator %s at '%s'" % \
                                 (self._operators, self._text[self._start:]))

        # quoted string literal
        # XXX could allow quoted quotes?
        elif char in ['"', "'"]:
            ptr += 1
            literal = ""
            while ptr < tlen and self._text[ptr] != char:
                literal += self._text[ptr]
                ptr += 1
            if ptr >= tlen:
                raise LexerError("Unterminated string at '%s'" % \
                                 self._text[self._start:])
            self._end = ptr + 1
            self._current = ("literal", literal)

        # number (unsigned integer)
        # XXX need both signed and unsigned
        elif char.isdigit():
            number = 0
            while ptr < tlen and self._text[ptr].isdigit():
                number = 10 * number + int(self._text[ptr])
                ptr += 1
            self._end = ptr
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
            raise LexerError("Invalid token at '%s'" % \
                             self._text[self._start:])

class PathParser:
    # valid operators in expressions (can include names such as "in")
    _operators = ["=", "!="]

    def __init__(self, lexer):
        self._lexer = lexer

    def parse(self):
        return self._parse_comps()

    def _parse_comps(self):
        """comps : ( comp comp_term )...
        """

        comps = []
        while True:
            # XXX this is hiding some errors, e.g. ["]"
            try:
                comp = self._parse_comp()
                comps.append(comp)
                self._parse_comp_term()
            except EndOfInput:
                break

        return comps
            
    def _parse_comp_term(self):
        """comp_term : '.'
                     | EndOfInput (caught by caller)
        """
        
        (type, token) = self._lexer.next()
        if type != ".":
            raise ParserError("Expected '.' at '%s'" % self._lexer.rest())
    
    def _parse_comp(self):
        """comp : name
                | inst
        """
        
        (type, token) = self._lexer.peek()
        if type == "name":
            self._lexer.advance()
            comp = ("name", token)

        else:
            inst = self._parse_inst()
            comp = ("inst", inst)

        #print("comp", comp)
        return comp

    # XXX need to distinguish unsigned (for instance number) and signed (for
    #     value)
    def _parse_inst(self):
        """inst : number
                | '*'
                | exprs
        """
        
        (type, token) = self._lexer.peek()
        if type == "number":
            self._lexer.advance()
            inst = ("number", token)
            
        elif type == "*":
            self._lexer.advance()
            inst = ("wildcard", token)
            
        elif type == "[":
            exprs = self._parse_exprs()
            inst = ("exprs", exprs)
            
        else:
            raise ParserError("Invalid instance at %s" % self._lexer.rest())

        #print("  inst", inst)
        return inst

    # XXX could introduce a "pred" (predicate) level
    def _parse_exprs(self):
        """exprs : ( '[' expr ']' )...
        """

        exprs = []
        (type, token) = self._lexer.peek()
        while type == "[":
            self._lexer.advance()
            expr = self._parse_expr()
            exprs.append(expr)
            
            (type, token) = self._lexer.next()
            if type != "]":
                raise ParserError("Expected ']' at '%s'" % self._lexer.rest())

            # XXX it might be better to have an EOI (EndOfInput) token?
            try:
                (type, token) = self._lexer.peek()
            except EndOfInput:
                break

        #print("  exprs", exprs)
        return exprs

    # XXX allowing a bare name provides only partial support for the
    #     existing Alias syntax [ABC]
    # XXX name here needs to permit the A.B form
    # XXX should break out "name | value" into "alias" production
    def _parse_expr(self):
        """expr : name oper value
                | name
                | value
        """

        (type, token) = self._lexer.peek()
        if type == "name":
            self._lexer.advance()
            (type, temp) = self._lexer.peek()
            if temp == "]":
                expr = ("alias", token)
            else:
                oper = self._parse_oper()
                value = self._parse_value()
                expr = ("simple", (token, oper, value))

        else:
            value = self._parse_value()
            expr = ("alias", value)
                
        #print("    expr", expr)
        return expr

    def _parse_oper(self):
        """oper : '='
                | '!='
                | etc
        """

        (type, oper) = self._lexer.peek()
        if oper not in self._operators:
            raise ParserError("Expected operator %s at '%s'" % \
                              (str(self._operators), self._lexer.rest()))
        
        self._lexer.advance()

        return oper

    # XXX should try adding comps here (recursion)
    def _parse_value(self):
        """value : literal
                 | number
        """
        
        (type, value) = self._lexer.peek()
        if type not in ["literal", "number"]:
            raise ParserError("Expected value at '%s'" % self._lexer.rest())
        
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
    print(path)
    parser = PathParser(PathLexer(path))
    try:
        comps = parser.parse()
        for (i, comp) in enumerate(comps):
            print(" ", comp)
    except PathError as e:
        sys.stderr.write("%s: %s\n" % (e.__class__.__name__, e))
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
