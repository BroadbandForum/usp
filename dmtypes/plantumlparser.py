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

# parsed class tree (this is what's returned to the caller)

class Class:
    _classes = {}

    @staticmethod
    def get(name):
        # XXX yes I originally had Class._classes.get(name, Class(name)) and
        #     then wondered why no class had more than one relationship!
        return Class._classes.get(name) \
            if name in Class._classes else Class(name)

    @staticmethod
    def get_classes(): return Class._classes

    # XXX can one make a constructor private? simple answer: no
    #     http://stackoverflow.com/questions/25040834
    def __init__(self, name):
        self._name = name
        self._superclasses = []
        self._associations = []
        Class._classes[name] = self

    def add_relationship(self, relationship):
        class1 = relationship.get_class1()
        rolecard1 = relationship.get_rolecard1()
        relation = relationship.get_relation()
        rolecard2 = relationship.get_rolecard2()
        class2 = relationship.get_class2()

        if class1 is not self:
            raise ValueError(class1)
        if relation not in (LAGGREGA, LAGGREG, LCOMPOSA, LCOMPOS, REXTENS):
            raise ValueError(relation)

        if relation == REXTENS:
            self._superclasses.append(class2)
        else:
            self._associations.append((class2, rolecard2))

    def get_name(self): return self._name
        
    def __repr__(self):
        superclasses = ['%s' % s.get_name() for s in self._superclasses]

        associations = ['%s:%s%s' % (r.get_role(c.get_name()), c.get_name(),
                                     r.get_card_string())
                        for c, r in self._associations]

        info = ''
        info += '(%s)' % ','.join(superclasses) if superclasses else ''
        info += ' %s' % ' '.join(associations) if associations else ''
        
        return '<Class %s%s>' % (self._name, info)

class Relationship:
    def __init__(self, class1, rolecard1, relation, rolecard2, class2):   
        self._class1 = class1
        self._rolecard1 = rolecard1
        self._relation = relation
        self._rolecard2 = rolecard2
        self._class2 = class2
        class1.add_relationship(self)

    def get_class1(self): return self._class1
    def get_rolecard1(self): return self._rolecard1
    def get_relation(self): return self._relation
    def get_rolecard2(self): return self._rolecard2
    def get_class2(self): return self._class2
        
    def __repr__(self):
        return '<Relationship %s %s %s %s %s>' % \
            (self._class1.get_name(), self._rolecard1, self._relation,
             self._rolecard2, self._class2.get_name())

class RoleCard:
    def __init__(self, role, card):
        self._role = role
        self._card = card

    # XXX better to have a Card class
    def _get_card_tuple(self):
        card = self._card
        # XXX assumes len(card) is 2 if tuple
        return card if type(card) is tuple else (card, card)
    
    def get_card_string(self):
        (min, max) = self._get_card_tuple()
        return '' if max == min and max == 1 else \
            max if max == min else '[%s..%s]' % (min, max)
        
    def get_role(self, class_name=None):
        if self._role:
            return self._role
        elif class_name:
            role = class_name.lower()
            (min, max) = self._get_card_tuple()
            if max == '*' or max > 1: role += 's'
            return role
        else:
            return None

    def get_card(self): return self._card
        
    def __repr__(self):
        return '<RoleCard %s %s>' % (self._role, self._card)

# lexing rules

# XXX shouldn't use so many (or any) reserved words
reserved = {
    'abstract': 'ABSTRACT',
    'class':    'CLASS',
    'define':   'DEFINE',
    'else':     'ELSE',
    'empty':    'EMPTY',
    'endif':    'ENDIF',
    'enduml' :  'ENDUML',
    'fields':   'FIELDS',
    'hide':     'HIDE',
    'ifdef':    'IFDEF',
    'methods':  'METHODS',
    'startuml': 'STARTUML'
}

tokens = ['DOTDOT', 'LAGGREGA', 'LAGGREG', 'RAGGREGA', 'RAGGREG',
          'LCOMPOSA', 'LCOMPOS', 'RCOMPOSA', 'RCOMPOS',
          'LEXTENS', 'REXTENS', 'NAME', 'ESCAPE', 'NUMBER', 'EOL'] + \
    list(reserved.values()) 

t_DOTDOT   = r'\.\.'
t_ESCAPE   = r'\\[a-z]'

#t_LAGGREGA = r'o-->'
#t_LAGGREG  = r'o--'
t_RAGGREGA = r'<--o'
t_RAGGREG  = r'--o'
t_LCOMPOSA = r'\*-->'
t_LCOMPOS  = r'\*--'
t_RCOMPOSA = r'<--\*'
t_RCOMPOS  = r'--\*'
t_LEXTENS  = r'<\|--'
t_REXTENS  = r'--\|>'

# XXX should do something cleverer here (c.f. reserved words) that avoids
#     need for later swapping logic
LAGGREGA = r'o-->'
LAGGREG  = r'o--'
RAGGREGA = r'<--o'
RAGGREG  = r'--o'
LCOMPOSA = r'*-->'
LCOMPOS  = r'*--'
RCOMPOSA = r'<--*'
RCOMPOS  = r'--*'
LEXTENS = r'<|--'
REXTENS = r'--|>'

literals = r'!@:"+{}()*'

def t_COMMENT(t):
    r'\'.*'
    pass

# XXX this is to ensure that LAGGREGA and LAGGREG are tokenized correctly;
#     need to use functions to ensure they are checked before NAME
def t_LAGGREGA(t):
    r'o-->'
    return t

def t_LAGGREG(t):
    r'o--'
    return t

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
                         | '!' ELSE EOL
                         | '!' ENDIF EOL'''

def p_hide_directive(t):
    '''hide_directive : HIDE EMPTY FIELDS EOL
                      | HIDE EMPTY METHODS EOL'''

def p_class_statement(t):
    '''class_statement : class_abstract CLASS class_name class_body EOL'''

def p_class_abstract(t):
    '''class_abstract : ABSTRACT
                      | empty'''
    
def p_class_name(t):
    '''class_name : NAME'''
    t[0] = Class.get(t[1])
    
def p_class_body(t):
    '''class_body : '{' EOL fields_and_methods '}'
                  | empty'''
    t[0] = t[3] if len(t) > 3 else None
    
def p_fields_and_methods(t):
    '''fields_and_methods : fields methods'''
    t[0] = (t[1], t[2])
    
def p_fields(t):
    '''fields : empty
              | field
              | fields field'''
    
def p_field(t):
    '''field : visibility NAME ':' NAME field_options EOL'''

def p_visibility(t):
    '''visibility : '+'
                 | empty'''
    
def p_field_options(t):
    '''field_options : '{' NAME '}'
                     | empty'''

def p_methods(t):
    '''methods : empty
               | method
               | methods method'''
    
def p_method(t):
    '''method : visibility NAME '(' ')' method_result method_modifiers EOL'''

def p_method_result(t):
    '''method_result : ':' NAME
                     | empty'''
    
def p_method_modifiers(t):
    '''method_modifiers : empty
                        | method_modifier
                        | method_modifiers method_modifier'''

def p_method_modifier(t):
    '''method_modifier : '{' ABSTRACT '}'
                       | '{' NAME '}' '''
    
# XXX should treat extension separately because role_and_card doesn't apply?
def p_class_rel(t):
    '''class_rel : NAME role_and_card rel role_and_card NAME EOL'''
    cl1 = Class.get(t[1])
    rc1 = t[2]
    rel = t[3]
    rc2 = t[4]
    cl2 = Class.get(t[5])
    # for LAGGREG, LCOMPOS and REXTENS, the first class references the second
    if rel not in (LAGGREGA, LAGGREG, LCOMPOSA, LCOMPOS, REXTENS):
        cl1, cl2 = cl2, cl1
        rc1, rc2 = rc2, rc1
        rel = {RAGGREGA: LAGGREGA, RAGGREG: LAGGREG,
               RCOMPOSA: LCOMPOSA, RCOMPOS: LCOMPOS, LEXTENS: REXTENS}[rel]
    t[0] = Relationship(cl1, rc1, rel, rc2, cl2)

def p_role_and_card(t):
    '''role_and_card : '"' role_then_card '"'
                     | '"' card_then_role '"'
                     | empty'''
    t[0] = t[2] if len(t) > 2 else None

def p_role_then_card(t):
    '''role_then_card : role escape card'''
    t[0] = RoleCard(t[1], t[3])
    
def p_card_then_role(t):
    '''card_then_role : card escape role'''
    t[0] = RoleCard(t[3], t[1])
    
def p_role(t):
    '''role : NAME
            | empty'''
    t[0] = t[1]
    
def p_escape(t):
    '''escape : ESCAPE
              | empty'''
    
def p_card(t):
    '''card : card_number
            | card_number DOTDOT card_number
            | empty'''
    t[0] = (t[1], t[3]) if len(t) > 2 else t[1] if len(t) > 1 else None

def p_card_number(t):
    '''card_number : NUMBER
                   | '*' '''
    t[0] = t[1]
    
def p_rel(t):
    '''rel : LAGGREGA
           | LAGGREG
           | RAGGREGA
           | RAGGREG
           | LCOMPOSA
           | LCOMPOS
           | RCOMPOSA
           | RCOMPOS
           | LEXTENS
           | REXTENS'''
    t[0] = t[1]
    
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
        classes = parse(arg, lexonly)
        for name, class_ in classes.items():
            print(class_)

if __name__ == "__main__":
    sys.exit(main())
