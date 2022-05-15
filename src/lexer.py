#####
# Constants
#####
VERSION = '0.0.0'

import math, sys
from .funcs import *
from .errors import *


def escape(text):
  return text.replace('\n', '\\n').replace('\t', '\\t')

#####
# Tokens
#####
token_types = {
  '+': 'PLUS',
  '-': 'MINUS',
  '*': 'MULT',
  '/': 'DIV',
  '^': 'EXP',
  '%': 'MOD',
  '(': 'LPAREN',
  ')': 'RPAREN',
  '[': 'LBRACKET',
  ']': 'RBRACKET',
  '{': 'LCURLY',
  '}': 'RCURLY',
  ':': 'COLON',
  ';': 'SEMICOL',
  ',': 'COMMA',

  '\\': 'BSLASH',
  
  'INT':   'INT',
  'FLOAT': 'FLOAT',
  'STR':   'STR',

  'VAR': 'VAR'
}

# token_types_2 = {
#   '||': 'OR',
#   '&&': 'AND',
#   '==': 'EQUALS'
# }

DIGITS       = '0123456789.'
ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.0123456789'

#####
# Parser
#####
class Position():
  def __init__(self, idx, ln, col, fn, ftxt):
    self.idx = idx
    self.ln = ln
    self.col = col
    self.fn = fn
    self.ftxt = ftxt

  def advance(self, char):
    self.idx += 1
    self.col += 1
    if char == '\n':
      self.ln += 1
      self.col = 0
    return self

  def reverse(self, char):
    self.idx -= 1
    self.col -= 1
    return self

  def copy(self):
    return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


class ParseResult():
  def __init__(self):
    self.node = None

  def register(self, res):
    return res
    


class Token():
  def __init__(self, type_, value=None, length=1, p=None):
    self.type = type_
    self.value = value
    self.length = 1    
    self.p = p

  def __repr__(self):
    if self.value: return f'{self.type}:{self.value}'
    return f'{self.type}'



class Lexer():
  def __init__(self, fn, text, env={}):
    self.fn = fn
    self.t = text
    self.p = Position(-1, 0, -1, fn, text)
    self.char = None
    self.env = env
    self.advance()

  def advance(self):
    self.p.advance(self.char)
    self.char = self.t[self.p.idx] if self.p.idx < len(self.t) else None

  def reverse(self):
    self.p.reverse(self.char)
    self.char = self.t[self.p.idx] if self.p.idx < len(self.t) else None
  
  def make_tokens(self):
    tokens = []
    while self.char != None:
      if self.char in ' \t':
        self.advance() # Ignore
      elif self.char in ';\n':
        tokens.append(Token('NEWLINE'))
        self.advance()
      elif self.char in token_types.keys():
        tokens.append(Token(token_types[self.char]))
        self.advance()
      elif self.char in DIGITS:
        tokens.append(self.make_num())
        self.advance()
      elif self.char in ALPHANUMERIC:
        tokens.append(self.make_var(self.p.copy()))
      else:
        cp = self.p.copy()
        Raise.__call__(SyntaxError, f"Unidentified character '{escape(self.char)}'", cp.fn, cp.ln, cp.col, cp.ftxt)
        self.advance()
        return []
    return tokens

  def make_num(self):
    num_str = ''
    periods = 0
    while self.char != None and self.char in DIGITS:
      if self.char == '.':
        if periods >= 1: break
        periods += 1
        num_str += '.'
      else:
        num_str += self.char
      self.advance()

    if periods == 0:
      return Token(token_types['INT'], INT(int(num_str)))

    else:
      if num_str != '.':
        return Token(token_types['FLOAT'], FLOAT(float(num_str)))
      else:
        cp = self.p.copy()
        Raise.__call__(SyntaxError, f"Ignoring unidentified character '.'", cp.fn, cp.ln, cp.col-1, cp.ftxt)
        return Token(token_types['FLOAT'], FLOAT(float(0)))

  def make_var(self, p=Position(-1, 0, 0, '', '')):
    var_str = ''
    while self.char != None and self.char in ALPHANUMERIC:
      var_str += self.char
      self.advance()
    return Token(token_types['VAR'], self.read_var(var_str, self.env), p=p)

  def read_var(self, v='', env={}):
    parent = v.split('.')[0]
    leftover = v[len(parent)+1:]
    var = None
    if parent in list(env.keys()):
      var = env[parent]
    else:
      cp = self.p.copy()
      Raise.__call__(NameError, f"Name '{parent}' is not defined.", cp.fn, cp.ln, cp.col-len(v), cp.ftxt, len(parent))
      return
    leftover = leftover.split('.')
    index = 0
    for i in leftover:
      if i != '':
        if i in var.__dir__(var):
          var = getattr(var, i)
        else:
          parent_name = parent
          for item in range(0, index):
            parent_name += '.' + leftover[item]
          cp = self.p.copy()
          Raise.__call__(NameError, f"Name '{parent_name}' has no attribute '{i}'", cp.fn, cp.ln, len(parent_name)+1, cp.ftxt, len(i))
          return
      index += 1
    return var
      

#####
# Nodes
#####
class NumberNode():
  def __init__(self, tok):
    self.tok = tok

  def __repr__(self):
    return f'{self.tok}'

class BinOpNode():
  def __init__(self, left_node, op_node, right_node):
    self.l = left_node
    self.o = op_node
    self.r = right_node

  def __repr__(self):
    return f'({self.l}, {self.o}, {self.r})'

class UnaryOpNode():
  def __init__(self, op_tok, node):
    self.o = op_tok
    self.node = node

  def __repr__(self):
    return f"{self.o}, {self.node}"

class VarNode():
  def __init__(self, tok, o=None):
    self.tok = tok
    self.out = o

  def __repr__(self):
    if self.out: return self.out.__tostring__()
    return self.tok.value.__tostring__()
    
    
#####
# Parser
#####
class Parser():
  def __init__(self, tokens, p):
    self.tokens = tokens
    self.idx = -1
    self.p = p
    self.advance()

  def update_curr(self):
    if self.idx >= 0 and self.idx < len(self.tokens):
      self.curr = self.tokens[self.idx]
  
  def advance(self):
    self.idx += 1
    self.update_curr()
    return self.curr

  def parse(self):
    return self.expr()
  
  def factor(self):
    res = ParseResult()
    tok = self.curr
    if tok.type == 'NEWLINE':
      return
    elif tok.type == token_types['VAR']:
      self.advance()
      if self.curr.type == token_types['(']:
        arguments = []
        c = True
        o = None
        while c:
          if self.curr.type != token_types[')']:
            if self.advance().type == token_types[')']:
              if not tok.value:
                pass
              elif tok.value.__type__ == 'func':
                try:
                  return VarNode(tok, tok.value.__call__())
                except python_error('TypeError'):
                  Raise.__call__(ArgumentError, f"{tok.value.__fname__} requires {len(tok.value.__call__.__code__.co_varnames)-tok.value.__call__.__code__.co_kwonlyargcount} argument(s).", tok.p.fn, tok.p.ln, tok.p.col, tok.p.ftxt, length=len(tok.value.__fname__))
              else:
                Raise.__call__(TypeError, f"'{tok.value.__fname__}' is of type {tok.value.__type__} and not func.")
              return
            else:
              self.factor()
            self.advance()
          else:
            c = False
        
      return VarNode(tok)
    elif tok.type in (token_types['+'], token_types['-']):
      res.register(self.advance())
      factor = res.register(self.factor())
      return UnaryOpNode(tok, factor)
    elif tok.type in (token_types['INT'], token_types['FLOAT']):
      res.register(self.advance())
      return NumberNode(tok)
    elif tok.type == token_types['(']:
      res.register(self.advance())
      expr = res.register(self.expr())
      if self.curr.type == token_types[')']:
        res.register(self.advance())
        return expr
      else:
        Raise.__call__(SyntaxError, f"Missing ')' at end of expression", cp.fn, cp.ln, 0, cp.ftxt, len(cp.ftxt.split('\n')[cp.ln-1]))
        return

  def bin_op(self, f, ops=()):
    l = f()
    while self.curr.type in ops:
      o = self.curr
      self.advance()
      r = f()
      l = BinOpNode(l, o, r)
    return l
  
  def term(self):
    return self.bin_op(self.factor, (token_types['^'], token_types['*'], token_types['/'], token_types['%']))

  def expr(self):
    return self.bin_op(self.term, (token_types['-'], token_types['+']))


#####
# Interpereter
####
class Interpereter():
  def get_method(self, node):
    return getattr(self, f"visit_{type(node).__name__}", self.no_method)

  def walkTree(self, node):
    return self.get_method(node)(node)

  def no_method(self, node):
    Raise.__call__(Error, f"No method defined for {type(node).__name__}.", 'Germanium Interpereter', 0, 0, 'None', 4, 3)

  def visit_NumberNode(self, node):
    return node.tok.value

  def visit_BinOpNode(self, node):
    num0 = self.get_method(node.l)(node.l)
    num1 = self.get_method(node.r)(node.r)

    int_or_float = lambda a, b: {True:INT,False:FLOAT}[a.__type__=='int' and b.__type__=='int']
    
    operation_type = {
      'PLUS': lambda a, b: int_or_float(a, b)(a.__value__ + b.__value__),
      'MINUS': lambda a, b: int_or_float(a, b)(a.__value__ - b.__value__),
      'MULT': lambda a, b: int_or_float(a, b)(a.__value__ * a.__value__),
      'DIV': lambda a, b: int_or_float(a, b)(a.__value__ / b.__value__),
      'MOD': lambda a, b: int_or_float(a, b)(a.__value__ % b.__value__),
      'EXP': lambda a, b: int_or_float(a, b)(a.__value__ ** b.__value__)
    }
    
    return (operation_type[node.o.type](num0, num1))
  
  def visit_UnaryOpNode(self, node):
    pyprint("Found unaryop node")

  def visit_VarNode(self, node):
    if node.out: return node.out
    return node.tok.value

  def visit_NoneType(self, node=None):
    return
    

#####
# Line Execution
#####
def Execute(fn, text, env={}):
  lexer = Lexer(fn, text, env)
  tokens = lexer.make_tokens()
  
  parser = Parser(tokens, lexer.p)
  ast = parser.parse()

  interp = Interpereter()
  out = interp.walkTree(ast)
  
  return out