#!/usr/bin/env python3
#
# module layout is as recommended at
# http://www.artima.com/weblogs/viewpost.jsp?thread=4829
#
# inspired by PLY example at
# http://www.dabeaz.com/ply/example.html

'''Experimental PlantUML parser.

Currently supports only a subset of the PlantUML class diagram syntax.
'''

import getopt
import logging
import sys

import ply.lex as lex
import ply.yacc as yacc

# set to True to enable creating parser.out and other output
debug = False

# set to True to enable creating parsetab.py
write_tables = False

# parsed class tree (this is what's returned to the caller

class Class:
    _classes = []

    def __init__(self, name, body):
        self._name = name
        self._body = body
        Class._classes.append(self)

    @staticmethod
    def get_classes():
        return Class._classes
        
    def __repr__(self):
        return '<Class %s>' % self._name

# lexing rules

# XXX shouldn't use so many (or any) reserved words
reserved = {
    'class':    'CLASS',
    'define':   'DEFINE',
    'empty':    'EMPTY',
    'endif':    'ENDIF',
    'enduml' :  'ENDUML',
    'fields':   'FIELDS',
    'hide':     'HIDE',
    'ifdef':    'IFDEF',
    'methods':  'METHODS',
    'startuml': 'STARTUML'
}

tokens = ['DOTDOT', 'LAGGREG', 'RAGGREG', 'LCOMPOS', 'RCOMPOS',
          'LEXTENS', 'REXTENS', 'NAME', 'ESCAPE', 'NUMBER', 'EOL'] + \
    list(reserved.values()) 

t_DOTDOT  = r'\.\.'
t_ESCAPE  = r'\\[a-z]'
t_LAGGREG = r'o--'
t_RAGGREG = r'--o'
t_LCOMPOS = r'\*--'
t_RCOMPOS = r'--\*'
t_LEXTENS = r'<\|--'
t_REXTENS = r'--\|>'

literals = r'!@:"+{}()'

def t_COMMENT(t):
    r'\'.*'
    pass

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_EOL(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    t.value = '\\n'
    return t
    
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex(debug=debug)

# parsing rules

def p_statements(t):
    '''statements : statement
                  | statement statements'''

def p_statement(t):
    '''statement : at_directive
                 | preproc_directive
                 | hide_directive
                 | class_statement
                 | class_rel
                 | EOL'''

def p_at_directive(t):
    '''at_directive : '@' STARTUML EOL
                    | '@' ENDUML EOL'''

def p_preproc_directive(t):
    '''preproc_directive : '!' DEFINE NAME EOL
                         | '!' IFDEF NAME EOL
                         | '!' ENDIF EOL'''

def p_hide_directive(t):
    '''hide_directive : HIDE EMPTY FIELDS EOL
                      | HIDE EMPTY METHODS EOL'''

def p_class_statement(t):
    '''class_statement : CLASS NAME class_body EOL'''
    t[0] = Class(t[2], t[3])

def p_class_body(t):
    '''class_body : '{' EOL fields_and_methods '}'
                  | empty'''
    
def p_fields_and_methods(t):
    '''fields_and_methods : fields methods'''
    
def p_fields(t):
    '''fields : empty
              | field
              | fields field'''
    
def p_field(t):
    '''field : '+' NAME ':' NAME field_options EOL'''

def p_field_options(t):
    '''field_options : '{' NAME '}'
                     | empty'''

def p_methods(t):
    '''methods : empty
               | method
               | methods method'''
    
def p_method(t):
    '''method : '+' NAME '(' ')' EOL'''

def p_class_rel(t):
    '''class_rel : NAME role_and_card rel role_and_card NAME EOL'''

def p_role_and_card(t):
    '''role_and_card : '"' role card '"'
                     | empty'''

def p_role(t):
    '''role : NAME
            | NAME ESCAPE
            | empty'''
    
def p_card(t):
    '''card : card_number
            | card_number DOTDOT card_number
            | empty'''

def p_card_number(t):
    '''card_number : NUMBER
                   | '*' '''
    
def p_rel(t):
    '''rel : LAGGREG
           | RAGGREG
           | LEXTENS
           | REXTENS
           | LCOMPOS
           | RCOMPOS'''
    
def p_empty(p):
    '''empty :'''
    pass

def p_error(t):
    print("%d: syntax error at '%s'" % (t.lexer.lineno, t.value))

parser = yacc.yacc(debug=debug, write_tables=write_tables)

def parse(file, lexonly=False):
    data = open(file).read()

    if lexonly:
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: 
                break
            print(tok)

    else:
        parser.parse(data)
        return Class.get_classes()

def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl",
                                   ["help", "lexonly"])

    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)

    lexonly = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif o in ("-l", "--lexony"):
            lexonly = True

    for arg in args:
        print(parse(arg, lexonly))

if __name__ == "__main__":
    sys.exit(main())
