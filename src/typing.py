pyprint = print
#####
# Main class
#####
class MainType():
  def __init__(self):
    self.__type__ = ''
    self.__name__ = ''
    self.__fdoc__ = ''
  def __tostring__(self):
    return STR(f"<{self.__type__} {self.__name__}>")

#####
# Object Types
#####
class NONE(MainType):
  def __init__(self):
    super().__init__()
    self.__type__ = 'none'
    self.__name__ = 'None'
    
  def __tostring__():
    return STR("None")

class BOOL(MainType):
  def __init__(self, v=True):
    super().__init__()
    self.__type__ = 'bool'
    self.__value__ = bool(v)
    self.__fdoc__ = 'This is a boolean. This means it has a true or \
                    false value.'
  def __tostring__(self):
    return STR(str(self.__value__).lower())

class FUNC(MainType):
  __type__ = 'func'
  __name__ = ''
  def __tostring__():
    return STR(f"<func {__name__}>")
  def __call__():
    pass

class INT(MainType):
  def __init__(self, v=0):
    super().__init__()
    self.__type__ = 'int'
    self.__value__ = v
  def __tostring__(self):
    return STR(self.__value__)

class FLOAT(MainType):
  def __init__(self, v=0.0):
    super().__init__()
    self.__type__ = 'float'
    self.__value__ = v
  def __tostring__(self):
    return STR(self.__value__)

class STR(MainType):
  def __init__(self, v=''):
    super().__init__()
    self.__type__ = 'str'
    self.__value__ = str(v)
  def __tostring__(self):
    return STR(self.__value__)

class LIST(MainType):
  def __init__(self, v=[]):
    super().__init__()
    self.__type__ = 'list'
    self.__value__ = list(v)
  def __tostring__(self):
    return STR(str(self.__value__))

class Error(MainType):
  __type__ = 'err'
  __name__ = 'Error'
  __details__ = 'An error occurred.'
  def __tostring__(details=''):
    if details == '': details = Error.__details__
    return f'[{Error.__name__}] {details}'

__builtin__ = {}

if str(type(__builtins__)) == "<class 'module'>":
  for i in __builtins__.__dir__():
    __builtin__[i] = getattr(__builtins__, i)

