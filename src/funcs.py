class PythonReturn(Exception):
  pass

from .typing import *
from .errors import *
import sys

def python_error(err='Exception'):
  try:
    return __builtins__[err]
  except:
    return getattr(__builtins__, err)

class print(FUNC):
  __name__ = 'print'
  __fname__ = 'print'
  def __call__(s=STR(), end=STR('\n')):
    f = open('/dev/stdout', 'w')
    f.write(s.__tostring__().__value__ + end.__tostring__().__value__)
    f.close()
  def __tostring__():
    return STR("<func builtin:print>")

class quit(FUNC):
  __name__ = 'quit'
  __fname__ = 'quit'
  def __call__(status=INT(0)):
    sys.exit(status.__value__)
  def __tostring__():
    return STR("<func builtin:quit>\nUse quit() to exit.")

class python(FUNC):
  __name__ = 'python'
  __fname__ = 'python'
  def __call__():
    raise PythonReturn
  def __tostring__():
    return STR('Returns to the python runtime environment.')

class Help_Message():
  __fdoc__ = STR("This is the help function. Type help() for help, or \
             help(object) for help on a specific object.")
    
class Help(FUNC):
  __name__ = 'help'
  __fname__ = 'help'
  __fdoc__ = STR("This is the help function. Type help() for help, or \
             help(object) for help on a specific object.")
  def __call__(status=Help_Message):
    try:
      return status.__fdoc__
    except python_error('AttributeError') as ae:
      Raise.__call__(AttributeError, str(ae), '<func help>', 0, 0, '__fdoc__', 8)

def EnvDirGen(e={}):
  class EnvDir(FUNC):
    __name__ = '__dir__'
    __fname__ = '__dir__'
    __type__ = 'func'
    def __call__():
      return LIST(list(e.keys()))
  return EnvDir

class Dir(FUNC):
  __name__ = 'dir'
  __fname__ = 'dir'
  def __call__(obj):
    return LIST(getattr(obj, '__dir__')(obj))

class Getattr(FUNC):
  __name__ = 'getattr'
  __fname__ = 'getattr'
  def __call__(o, s=STR()):
    return getattr(o, s)

class Raise(FUNC):
  __name__ = 'raise'
  __fname__ = 'raise'
  __fdoc__ = "Execute an error"
  def __call__(err_type=Error, details='', fn='<stdin>', ln=1, col=0, txt='', length=1, indent=0):
    nl = '\n'
    up = '^'
    ftxt_list = txt.split(nl)
    def get_line(index):
      try:
        if ln-index >= 0:
          return '  '*(indent+2) + ftxt_list[ln-index] + nl
        else:
          raise(python_error('IndexError'))
      except python_error('IndexError'):
        return ''
    msg = f"\033[31m\
{'  '*indent}Traceback (most recent call last):\n\
{'  '*indent}  File \"{fn}\", line {ln}, col {col+1}:\n\
{'  '*indent}    {err_type.__tostring__(details)}\n\
{get_line(2)}{get_line(1)}{get_line(0)}\
{'  '*indent}    {' '*col}{up*length}\
    \033[0m"
    print.__call__(STR(msg))


# Typing Functions
class String(FUNC):
  __name__ = 'String'
  __fname__ = 'String'
  def __call__(obj):
    return obj.__tostring__()

class Integer(FUNC):
  __name__ = 'Integer'
  __fname__ = 'Integer'
  def __call__(obj):
    return INT(obj.__value__)

class Float(FUNC):
  __name__ = 'Float'
  __fname__ = 'Float'
  def __call__(obj):
    return FLOAT(obj.__value__)

class Bool(FUNC):
  __name__ = 'Bool'
  __fname__ = 'Bool'
  def __call__(obj):
    return BOOL(obj.__value__)

class List(FUNC):
  __name__ = 'List'
  __fname__ = 'List'
  def __call__(obj):
    return LIST(obj.__value__)

## Debug Command (Run germanium functions with python)
def pyf(f, *args, **kwargs):
  return f.__call__(*args, **kwargs)

