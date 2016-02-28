#!/usr/bin/env python3

"""Experiment with parsing USP data model paths."""

class PathError(Exception):
    pass

class LexerError(PathError):
    pass

class ParserError(PathError):
    pass

class EndOfInput(PathError):
    pass

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
                raise LexerError("Invalid operator at '%s'" % \
                                 self._text[self._start:])

        # quoted string
        # XXX could allow quoted quotes?
        elif char in ['"', "'"]:
            ptr += 1
            string = ""
            while ptr < tlen and self._text[ptr] != char:
                string += self._text[ptr]
                ptr += 1
            if ptr >= tlen:
                raise LexerError("No closing quote at '%s'" % \
                                 self._text[self._start:])
            self._end = ptr + 1
            self._current = ("string", string)

        # number (unsigned integer)
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
            comp = self._parse_comp()
            comps.append(comp)

            try:
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
            raise ParserError("Invalid instance at %s", self._lexer.rest())

        #print("  inst", inst)
        return inst

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
            
            (type, token) = self._lexer.peek()

        #print("  exprs", exprs)
        return exprs

    # XXX allowing a bare name introduces an ambiguity and is a bad idea, so
    #     it's been disabled; this means that existing Alias syntax [ABC]
    #     isn't supported (must quote strings)
    def _parse_expr(self):
        """expr : name oper value
                | name (if not followed by oper)
                | value
        """

        (type, token) = self._lexer.peek()
        if type == "name":
            self._lexer.advance()
            name = ("name", token)
            oper = self._parse_oper()
            value = self._parse_value()
            expr = ("paramtest", (name, oper, value))
            #try:
            #    oper = self._parse_oper()
            #except ParserError:
            #    oper = None
            #    expr = ("defkey", name)
            #if oper is not None:
            #    value = self._parse_value()
            #    expr = ("paramtest", (name, oper, value))

        else:
            value = self._parse_value()
            expr = ("defkey", value)
                
        #print("    expr", expr)
        return expr

    # XXX could permit boolean constants
    def _parse_value(self):
        """value : string
                 | number
                 | boolean?
        """
        
        (type, token) = self._lexer.peek()
        if type not in ["string", "number"]:
            raise ParserError("Expected value at '%s'" % self._lexer.rest())
        
        self._lexer.advance()
        value = ("value", token)

        return value

    def _parse_oper(self):
        """oper : '='
                | '!='
                | etc
        """

        (type, value) = self._lexer.peek()
        if value not in self._operators:
            raise ParserError("Expected operator %s at '%s'" % \
                              (str(self._operators), self._lexer.rest()))
        
        self._lexer.advance()
        oper = ("oper", value)

        return oper

tree = {
    "Device": {
        "IP": {
            "Interface": {
                "{i}": None,
                1: {
                    "Name": "lan",
                    "Enable": False
                },
                2: {
                    "Name": "wan",
                    "Enable": True
                },
            },
        },
    },
}

path = 'Device.IP.Interface.[Name="lan"].Enable'
path = 'Device.IP.Interface.*.Enable'

parser = PathParser(PathLexer(path))
comps = parser.parse()

print(path)
text = ''
dict = tree
for comp in comps:
    print(comp)
    (type, value) = comp
    if type == "name":
        if value not in dict:
            print(value, "not in", list(dict.keys()))
        else:
            #print(" ", value, "found")
            text += value + "."
            dict = dict[value]
    elif type == "inst":
        (type, value) = value
        if "{i}" not in dict:
            print(" ", "not a table")
        else:
            inst = 2
            print(" ", "Need to evaluate; assume", inst)
            text += str(inst) + "."
            dict = dict[inst]
print(text)
