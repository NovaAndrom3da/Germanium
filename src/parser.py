VERSION = '0.0.0'

pyprint = print

import sly, sys, math, re
from .funcs import *

def remove_quotes(s=''):
  return STR(s[1:][:-1])

walkTreeVariable = {
  int: INT,
  str: STR
}


class GermaniumLexer(sly.Lexer):
  def __init__(self):
    self.nest = 0
  
  tokens = { NAME, NUMBER, STRING, EQUALS,
            LPAR, RPAR, #IF, ELSE, MEMBERS,
            BOOL, PARAM }
  ignore = '\t '
  literals = {
    '=', '+', '-', '/', 
    '*', '(', ')', ',', ';',
    '%', '^', '.'
  }

  NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
  STRING = r'(\".*?\")|(\'.*?\')'

  LPAR = r'\('
  RPAR = r'\)'

  #NAME['if'] = IF
  #NAME['else'] = ELSE
  # IF = "(if)\s"

  BOOL = "(\(true)|(true\))|(\strue\s)|(\(false)|(false\))|(\sfalse\s)"
  EQUALS = r'\=='

  @_(re.compile('.*', 0))
  def PARAM(self, t):
    return t
  
  @_(r'\d+')
  def NUMBER(self, t):
    t.value = int(t.value) 
    return t

  @_(r'//.*')
  def COMMENT(self, t):
    pass

  @_(r'\n+')
  def newline(self, t):
    self.lineno = t.value.count('\n')

class GermaniumParser(sly.Parser):
  # debugfile = 'parser.out'
  tokens = GermaniumLexer.tokens

  precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^', '%'),
    ('right', 'UMINUS', '.'),
  )
  
  def __init__(self):
    self.env = { }

  @_('')
  def statement(self, p):
    pass

  @_('NAME LPAR PARAM RPAR')
  def expr(self, p):
    pyprint(p.PARAM)
    return ('var_call', p.NAME, p.PARAM)
  
  @_('"." NUMBER')
  def expr(self, p):
    return ('float', p.NUMBER)
  
  @_('NUMBER "." NUMBER')
  def expr(self, p):
    return ('float', p.NUMBER0, p.NUMBER1)

  @_('STRING')
  def expr(self, p):
    return ('str', p.STRING)
  
  @_('var_assign')
  def statement(self, p):
    return p.var_assign

  @_('BOOL')
  def expr(self, p):
    return p.BOOL
  
  @_('NAME "=" expr')
  def var_assign(self, p):
    return ('var_assign', p.NAME, p.expr)

  # @_("IF BOOL NAME")
  # def if_statement(self, p):
  #   return ('if', p.BOOL)

  # @_('IF BOOL statement ELSE statement')
  # def if_else_statement(self, p):
  #   return p.statement

  @_('NAME "=" STRING')
  def var_assign(self, p):
    return ('var_assign', p.NAME, p.STRING)

  @_('expr')
  def statement(self, p):
    return (p.expr)

  @_('expr "+" expr')
  def expr(self, p):
    return ('add', p.expr0, p.expr1)

  @_('expr "-" expr')
  def expr(self, p):
    return ('sub', p.expr0, p.expr1)

  @_('expr "*" expr')
  def expr(self, p):
    return ('mul', p.expr0, p.expr1)

  @_('expr "/" expr')
  def expr(self, p):
    print(p.expr0, p.expr1)
    return ('div', p.expr0, p.expr1)

  @_('expr "%" expr')
  def expr(self, p):
    return ('mod', p.expr0, p.expr1)

  @_('expr "^" expr')
  def expr(self, p):
    return ('exp', p.expr0, p.expr1)

  @_('"-" expr %prec UMINUS')
  def expr(self, p):
    return p.expr

  @_('expr EQUALS expr')
  def expr(self, p):
    return ('equals', p.expr0, p.expr1)

  @_('NAME "." NAME')
  def expr(self, p):
    return ('sub_obj', p.NAME0, p.NAME1)
  
  @_('NAME LPAR RPAR')
  def expr(self, p):
    return ('var_call', p.NAME)

  @_('STRING "+" STRING')
  def expr(self, p):
    return ('cat', p.STRING0, p.STRING1)

  @_('LPAR expr RPAR')
  def expr(self, p):
    return p.expr
  
  @_('NAME')
  def expr(self, p):
    return ('var', p.NAME)

  @_('NUMBER')
  def expr(self, p):
    return ('num', p.NUMBER)





class GermaniumExecute:
  def __init__(self, tree, env):
    self.env = env
    result = self.walkTree(tree)
    if result is not None and isinstance(result, int):
      pyprint(result)
    if isinstance(result, str) and result[0] == '"':
      pyprint(result)

  def walkTree(self, node):
    if isinstance(node, int):
      return node
    if isinstance(node, str):
      return node

    if node is None:
      return None
    if node[0] == 'program':
      if node[1] == None:
        self.walkTree(node[2])
      else:
        self.walkTree(node[1])
        self.walkTree(node[2])

    if node[0] == 'num':
      return node[1]

    if node[0] == 'str':
      return node[1]

    if node[0] == 'bool':
      return str(node[1]).lower()

    if node[0] == 'add':
      return self.walkTree(node[1]) + self.walkTree(node[2])
    elif node[0] == 'sub':
      return self.walkTree(node[1]) - self.walkTree(node[2])
    elif node[0] == 'mul':
      return self.walkTree(node[1]) * self.walkTree(node[2])
    elif node[0] == 'div':
      return self.walkTree(node[1]) / self.walkTree(node[2])
    elif node[0] == 'mod':
      return self.walkTree(node[1]) % self.walkTree(node[2])
    elif node[0] == 'exp':
      return self.walkTree(node[1]) ** self.walkTree(node[2])
    elif node[0] == 'cat':
      return self.walkTree(node[1]) + self.walkTree(node[2])

    if node[0] == 'sub_obj':
      try:
        pyprint(self.walkTree(node[1]))
        return ('var', getattr(self.env[self.walkTree(node[1])], self.walkTree(node[2])))
      except:
        pyprint(f"[Error] Undefined variable '{node[1]}'")
    
    if node[0] == 'if':
      return node[1]

    if node[0] == 'float':
      try:
        whole = self.walkTree(node[1])
        decimal = self.walkTree(node[2])
      except IndexError:
        whole = 0
        decimal = self.walkTree(node[1])
      this_float = float(f"{whole}.{decimal}")
      pyprint(this_float)
      return (this_float)

    if node[0] == 'equals':
      return ('bool', self.walkTree(node[1]) == self.walkTree(node[2]))
    
    if node[0] == 'var_assign':
      val = self.walkTree(node[2])
      var = None
      if type(val) == str and (val.startswith('\'') or val.startswith('\"')) and (val.endswith('\'') or val.endswith('\"')):
        var = remove_quotes(val)
      else:
        var = walkTreeVariable[type(val)](val)
      self.env[node[1]] = var
      return var.__tostring__()

    if node[0] == 'var':
      try:
        var = self.env[node[1]]
        pyprint(var.__tostring__())
        return var.__tostring__()
      except LookupError:
        pyprint(f"[NameError] Undefined variable '{node[1]}'")

    if node[0] == 'var_call':
      args = []
      arguments = ''
      try: arguments = node[2]
      except: pass
      if not arguments == '':
        for i in arguments.split(','):
          args.append(i.lstrip().rstrip())
      pyprint(args)
      try:
        return self.env[node[1]].__call__(*args)
      except LookupError:
        pyprint(f"[NameError] Undefined variable '{node[1]}'")

## Define builtins
builtins = {
  '__VERSION__': STR(VERSION)
  "quit": quit,
  "print": print,
  "help": help,
  "Infinity": INT(math.inf),
  "String": String,
  "Integer": Integer,
  "Bool": Bool,
  "Float": Float,
  "true": BOOL(1),
  "false": BOOL(0),
  "py": python
}


def main():
  lexer = GermaniumLexer()
  parser = GermaniumParser()
  pyprint(f"Germanium v{VERSION}")
  env = builtins
  pyprint(env.__dir__())
    
  while True:    
    try:
      text = input('$ ')

    except KeyboardInterrupt:
      pyprint("\nKeyboardInterrupt")
      text = ""
    
    except EOFError:
      break
      
    if text:
      try:
        tree = parser.parse(lexer.tokenize(text))
        GermaniumExecute(tree, env)
      except KeyboardInterrupt:
        pyprint("KeyboardInterrupt")
      except sly.lex.LexError as e:
        pyprint(f"[SyntaxError] {str(e)}")
      except PythonReturn:
        break
      # except AttributeError as e:
      #   pyprint(f"[AttributeError] {e}")
      # except Exception as e:
      #   print.__call__(STR(f"[Error] {e}"))
      text = ''

if __name__ == "__main__": main()