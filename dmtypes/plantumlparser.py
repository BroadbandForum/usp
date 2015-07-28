#!/usr/bin/env python3
#
# module layout is as recommended at
# http://www.artima.com/weblogs/viewpost.jsp?thread=4829
#
# inspired by PLY example at
# http://www.dabeaz.com/ply/example.html

'''Experimental PlantUML class diagram parser.

Currently supports only a subset of the PlantUML syntax.
'''

import getopt
import sys

import ply.lex as lex
import ply.yacc as yacc

# XXX shouldn't use so many (or any) reserved words
reserved = {
    'startuml': 'STARTUML',
    'hide':     'HIDE',
    'empty':    'EMPTY',
    'fields':   'FIELDS',
    'methods':  'METHODS',
    'class':    'CLASS',
    'enduml' :  'ENDUML'
}

tokens = ['DOTDOT', 'LAGGREG', 'RAGGREG', 'LCOMPOS', 'RCOMPOS',
          'LEXTENS', 'REXTENS', 'NAME', 'NUMBER', 'EOL'] + \
    list(reserved.values()) 

t_DOTDOT  = r'\.\.'
t_LAGGREG = r'o--'
t_RAGGREG = r'--o'
t_LCOMPOS = r'\*--'
t_RCOMPOS = r'--\*'
t_LEXTENS = r'<\|--'
t_REXTENS = r'--\|>'

literals = r'@:"+{}()'

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
    
# ignored characters

t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# build the lexer

lexer = lex.lex()

# parsing rules

def p_statements(t):
    '''statements : statement
                  | statement statements'''

def p_statement(t):
    '''statement : at_directive
                 | hide_directive
                 | class_statement
                 | class_relationship
                 | EOL'''

def p_at_directive(t):
    '''at_directive : '@' STARTUML EOL
                    | '@' ENDUML EOL'''
    print('%s : %s %s' % (t[0], t[1], t[2]))

def p_hide_directive(t):
    '''hide_directive : HIDE EMPTY FIELDS EOL
                      | HIDE EMPTY METHODS EOL'''
    print('%s : %s %s %s' % (t[0], t[1], t[2], t[3]))

def p_class_statement(t):
    '''class_statement : CLASS NAME class_body EOL'''
    print('%s : %s %s' % (t[0], t[1], t[2]))    

def p_class_body(t):
    '''class_body : '{' EOL fields_and_methods '}' '''
    
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

def p_class_relationship(t):
    '''class_relationship : NAME arity relationship arity NAME EOL'''

def p_arity(t):
    '''arity : '"' NUMBER '"'
             | '"' NUMBER DOTDOT NUMBER '"'
             | empty'''

def p_relationship(t):
    '''relationship : LAGGREG
                    | RAGGREG
                    | LEXTENS
                    | REXTENS
                    | LCOMPOS
                    | RCOMPOS'''
    
def p_empty(p):
    '''empty :'''
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

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
        parse(arg, lexonly)

if __name__ == "__main__":
    sys.exit(main())
