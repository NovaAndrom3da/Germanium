# Import base error class
from .typing import Error

# Keys: Name of error, without 'Error'
# Values: Default description of error
_err_dict = {
  'Syntax': 'An error occurred.',
  'Name': 'Something was not defined.',
  'Type': 'The object is of a wrong type.',
  'Recursion': 'Recursion depth exceeded.',
  'Argument': 'The function recieved an improper number of arguments',
  'Attribute': 'The object does not have a specified attribute.'
}

# Error generator. Generates
# errors from _err_dict.
# This keeps from having a 
# whole file for repeated
# definitions
def _err_generator():
  glob = {'Error': Error}
  for i in _err_dict.keys():
    classstr = f"\
class {i}Error(Error):\n\
  __type__ = 'err'\n\
  __name__ = '{i}Error'\n\
  __fname__ = '{i}Error'\n\
  def __tostring__(details='{_err_dict[i]}'):\n\
    return f'[{i}Error] {'{'}details{'}'}'\
"
    exec(classstr, glob)
  return glob

# Fetch all errors from the generator
# and load them into the environment
_err_glob = _err_generator()
for _var in _err_glob.keys():
  exec(f"global {_var}")
  exec(f"{_var} = _err_glob['{_var}']")

