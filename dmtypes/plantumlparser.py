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

# XXX should change to use properties (no set_ and get_ methods)

# XXX should define a variable for the namespace separator; needs to be
#     consistent with PlantUML namespaceSeparator

# XXX should review what needs to be ordered and not; also what needs to be
#     checked for uniqueness and at what level

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

# XXX there is scope for a base class to deal with static list and/or dict
#     of instances, current instance etc

# XXX should note names be global or within the current namespace?
class Note:
    _notes = {}

    @staticmethod
    def find(name):
        return Note._notes.get(name, None)
        
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def __repr__(self):
        return '<Note %s %s>' % (self._name, self._value)

class Namespace:
    _namespaces = {}
    _current = None
    
    @staticmethod
    def open(name):
        return Namespace._namespaces.get(name) \
            if name in Namespace._namespaces else Namespace(name)

    @staticmethod
    def close():
        Namespace._current = None
        
    @staticmethod
    def get_current(): return Namespace._current

    def __init__(self, name):
        self._name = name
        self._parent = Namespace._current
        Namespace._current = self

    def get_path(self):
        if self._parent is None:
            return self._name
        else:
            return '%s.%s' % (self._parent.get_path(), self._name)

    def __repr__(self):
        return '<Namespace %s>' % self.get_path()

# XXX there is no explicit association with a Namespace object; instead the
#     current namespace is used to derive the fully-qualified item name; this
#     isn't ideal
class NamespacedItem:
    @staticmethod
    def get_full_name(name):
        current_namespace = Namespace.get_current()
        if name.startswith('.'):
            path = name[1:]
        elif not current_namespace:
            path = name
        else:
            path = '%s.%s' % (current_namespace.get_path(), name)
        return path

# XXX important: need a common base class for things that can be involved
#     in a relation: Enums and Classes (they will share a get() method)
    
# XXX not sure that need to keep track of all enums
class Enum(NamespacedItem):
    _enums = {}
    _current = None
    
    @staticmethod
    def get(name):
        full_name = Enum.get_full_name(name)
        return Enum._enums.get(full_name) \
            if full_name in Enum._enums else Enum(full_name)

    def __init__(self, name):
        self._name = name
        self._values = []
        Enum._enums[name] = self
        Enum._current = self
    
    @staticmethod
    def get_current(): return Enum._current

    def add_value(self, value):
        self._values.append(value)

    def __repr__(self):
        return '<Enum %s %s>' % (self._name, self._values)

class Class(NamespacedItem):
    _classes = {}
    _current = None
    
    @staticmethod
    def get(name):
        full_name = Class.get_full_name(name)
        return Class._classes.get(full_name) \
            if full_name in Class._classes else Class(full_name)

    @staticmethod
    def get_classes(): return Class._classes

    @staticmethod
    def get_current(): return Class._current

    # XXX can one make a constructor private? simple answer: no
    #     http://stackoverflow.com/questions/25040834
    def __init__(self, name):
        self._name = name
        self._notes = []
        self._fields = []
        self._methods = []
        self._superclasses = []
        self._associations = []
        Class._classes[name] = self
        Class._current = self

    def add_note(self, note):
        self._notes.append(note)

    def add_field(self, field):
        self._fields.append(field)
        
    def add_method(self, method):
        self._methods.append(method)
        
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

        notes = ' %s' % self._notes if self._notes else ''
        fields = ' %s' % self._fields if self._fields else ''
        methods = ' %s' % self._methods if self._methods else ''
        
        return '<Class %s%s%s%s%s>' % (self._name, info, notes, fields,
                                       methods)

# Field and Method could share a base class; should they know their Class?
class Field:
    def __init__(self, name, type, visibility, options):
        self._name = name
        self._type = type
        self._visibility = visibility
        self._options = options

    def __repr__(self):
        visibility = self._visibility if self._visibility else ''
        type = ':%s' % self._type if self._type else ''
        options = ' %s' % self._options if self._options else ''
        return '<Field %s%s%s%s>' % (visibility, self._name, type, options)
        
class Method:
    _current = None

    @staticmethod
    def get_current(): return Method._current

    def __init__(self, name, arguments, result, visibility, modifiers):
        self._name = name
        self._arguments = arguments
        self._result = result
        self._visibility = visibility
        self._modifiers = modifiers
        Method._current = self

    def __repr__(self):
        visibility = self._visibility if self._visibility else ''
        arguments = '(%s)' % self._arguments if self._arguments else '()'
        result = ':%s' % str(self._result) if self._result else ''
        modifiers = ' %s' % self._modifiers if self._modifiers else ''
        return '<Method %s%s%s%s%s>' % (visibility, self._name, arguments,
                                        result, modifiers)

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
            components = class_name.split('.')
            role = components[-1].lower()
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
    'as':       'AS',
    'class':    'CLASS',
    'define':   'DEFINE',
    'else':     'ELSE',
    'enum':     'ENUM',
    'empty':    'EMPTY',
    'endif':    'ENDIF',
    'enduml' :  'ENDUML',
    'fields':   'FIELDS',
    'hide':     'HIDE',
    'ifdef':    'IFDEF',
    'methods':  'METHODS',
    'namespace':'NAMESPACE',
    'note':     'NOTE',
    'startuml': 'STARTUML'
}

tokens = ['DOTDOT', 'LAGGREGA', 'LAGGREG', 'RAGGREGA', 'RAGGREG',
          'LCOMPOSA', 'LCOMPOS', 'RCOMPOSA', 'RCOMPOS',
          'LEXTENS', 'REXTENS',
          'QSTRING', 'ENDNOTE', 'REST', 'NAME',
          'ESCAPE', 'NUMBER', 'EOL'] + \
    list(reserved.values()) 

#t_DOTDOT   = r'\.\.'
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

literals = r'!@:"+{}()[]*'

states = (
    ('NOTE', 'inclusive'),
)

def t_NOTE(t):
    r'note'
    t.lexer.push_state('NOTE')
    return t    

def t_NOTE_ENDNOTE(t):
    r'end\s*note'
    t.lexer.pop_state()
    return t

# matches quoted string but removes the quotes
# XXX doesn't support escaped quotes within the string
def t_NOTE_QSTRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    t.lexer.pop_state()
    return t

def t_NOTE_REST(t):
    r'.+'
    return t

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

# XXX this is to ensure that DOTDOR is tokenized correctly (as above)
def t_DOTDOT(t):
    r'\.\.'
    return t

def t_NAME(t):
    r'[a-zA-Z_\.][a-zA-Z0-9_]*'
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
                 | other_statement'''

def p_at_directive(t):
    '''at_directive : '@' STARTUML EOL
                    | '@' ENDUML EOL'''

# XXX should support these
def p_preproc_directive(t):
    '''preproc_directive : '!' DEFINE NAME EOL
                         | '!' IFDEF NAME EOL
                         | '!' ELSE EOL
                         | '!' ENDIF EOL'''

def p_hide_directive(t):
    '''hide_directive : HIDE EMPTY FIELDS EOL
                      | HIDE EMPTY METHODS EOL'''

def p_other_statements(t):
    '''other_statements : empty
                        | other_statement
                        | other_statements other_statement'''
    
def p_other_statement(t):
    '''other_statement : ns_statement
                       | enum_statement
                       | class_statement
                       | class_rel
                       | note_statement
                       | EOL'''
    
def p_ns_statement(t):
    '''ns_statement : NAMESPACE ns_name '{' EOL ns_body '}' ns_close EOL'''

def p_ns_name(t):
    '''ns_name : NAME'''
    t[0] = Namespace.open(t[1])

def p_ns_body(t):
    '''ns_body : other_statements'''
    
def p_ns_close(t):
    '''ns_close : empty'''
    Namespace.close()
    
def p_enum_statement(t):
    '''enum_statement : ENUM enum_name '{' EOL values '}' '''

def p_enum_name(t):
    '''enum_name : NAME'''
    t[0] = Enum.get(t[1])
    
def p_values(t):
    '''values : empty
              | value
              | values value'''

def p_value(t):
    '''value : NAME EOL'''
    Enum.get_current().add_value(t[1])
    
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
    
def p_fields_and_methods(t):
    '''fields_and_methods : empty
                          | fld_or_mth
                          | fields_and_methods fld_or_mth'''

def p_fld_or_mth_eol(t):
    '''fld_or_mth : EOL'''
    
def p_field(t):
    '''fld_or_mth : visib NAME ':' NAME field_options EOL'''
    Class.get_current().add_field(Field(t[2], t[4], t[1], t[5]))

# XXX need to support multiple field options: {a} {b} syntax I think; should
#     check for the usual conventions and usual supported options
def p_field_options(t):
    '''field_options : '{' NAME '}'
                     | empty'''
    t[0] = [t[2]] if len(t) > 2 else []

def p_method(t):
    '''fld_or_mth : visib NAME '(' args ')' method_result method_mods EOL'''
    Class.get_current().add_method(Method(t[2], t[4], t[6], t[1], t[7]))

def p_method_result(t):
    '''method_result : ':' NAME
                     | ':' NAME '[' ']'
                     | empty'''
    t[0] = (t[2], (len(t) > 3)) if len(t) > 2 else None
    
def p_method_mods(t):
    '''method_mods : empty
                   | method_mod
                   | method_mods method_mod'''
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []
    else:
        t[1] = t[1].append(t[2])

# XXX need explicit ABSTRACT here because it's a reserved word :( 
def p_method_mod(t):
    '''method_mod : '{' ABSTRACT '}'
                  | '{' NAME '}' '''
    t[0] = t[2]

def p_args(t):
    '''args : empty
            | arg
            | args arg'''
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []
    else:
        t[1] = t[1].append(t[2])

# XXX needs to support array syntax and therefore use a common "type" rule
#     that is used for fields, return values and arguments
def p_arg(t):
    '''arg : NAME ':' NAME'''
    t[0] = (t[1], t[3])
    
# XXX need to add other visibility values
def p_visib(t):
    '''visib : '+'
             | empty'''
    t[0] = t[1]

# XXX should treat extension separately because role_and_card doesn't apply?
def p_class_rel(t):
    '''class_rel : NAME role_and_card rel role_and_card NAME rel_label EOL'''
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

# XXX should do something with this
def p_rel_label(t):
    '''rel_label : empty
                 | ':' NAME
                 | ':' '{' NAME '}' '''

# XXX PlantUML has many supported "note" syntaxes; some might be quite
#     challenging to tokenize
def p_note_statement_current(t):
    '''note_statement : NOTE REST EOL note_lines ENDNOTE EOL'''
    
def p_note_lines(t):
    '''note_lines : empty
                  | note_line
                  | note_lines note_line'''

def p_note_line(t):
    '''note_line : REST EOL'''
    Class.get_current().add_note(t[1])
    
def p_note_statement_named(t):
    '''note_statement : NOTE QSTRING AS NAME EOL'''
    Note(t[4], t[2])

def p_empty(t):
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
        if classes is not None:
            for name, class_ in classes.items():
                print(class_)

if __name__ == "__main__":
    sys.exit(main())
