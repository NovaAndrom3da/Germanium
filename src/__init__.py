import sys, os, platform

from .funcs import *
from .lexer import Execute, VERSION

def get_os_type():
  os_type = sys.platform
  if os_type == 'linux': # linux
    import distro
    return f"{distro.name()} {distro.version()} ({platform.machine()})"
  elif os_type == 'darwin': # macos
    return f"MacOS {platform.mac_ver()[0]} ({platform.machine()})"
  else: # windows and other operating systems
    return f"{platform.system()} {platform.release()} ({platform.machine()})"



env = {
  # Internal Variables
  '__version__': STR(VERSION),
  '__name__': '__main__',
  '__dir__': None,
  
  # Types
  'String': String,
  'Integer': Integer,
  'Bool': Bool,
  'Float': Float,
  'List': List,

  # Built-in Functions
  'print': print,
  'quit': quit,
  'help': Help,
  'dir': Dir,
  'getattr': Getattr,
  'raise': Raise,
  
  # Boolean Expressions
  'true': BOOL(1),
  'false': BOOL(0)
}

def execute(fn='', ftxt='', environ={}):
  try:
    exec = Execute(fn, ftxt, environ)
    return exec
  except python_error('KeyboardInterrupt'):
    pyprint('\nKeyboardInterrupt')
  except python_error('AttributeError') as ae:
    if str(ae) != "'Parser' object has no attribute 'curr'":
      raise(ae)
  except python_error('RecursionError'):
    Raise(RecursionError)



def main(mode='repl', fn=None, text=''):
  new_env = env.copy()
  new_env['__dir__'] = EnvDirGen(new_env)
  if mode == 'repl':
    # Set default build method
    build_type = f'Source, {platform.python_implementation()} {platform.python_version()}'

    # Set build method
    if "__compiled__" in globals():
      build_type = 'Compiled, Nuitka'


    
    pyprint(f"Germaium v{VERSION} [Build: {build_type}] on {get_os_type()}")
    while True:
      try:
        exec = execute('<stdin>', input('$ '), new_env)
        if exec: print.__call__(exec)
      except python_error('EOFError'):
        pyprint()
        sys.exit()
      except python_error('KeyboardInterrupt'):
        pyprint('\nKeyboardInterrupt')
  elif mode == 'file':
    new_env['__name__'] = fn
    f = open(fn)
    ftxt = f.read()
    f.close()
    exec = execute(fn, ftxt, new_env)
  elif mode == 'text':
    exec = execute('<stdin>', text, new_env)
    if exec: print.__call__(exec)
  elif mode == 'module':
    # do something different
    pass


if '-C' in sys.argv:
  main('text', text=" ".join(sys.argv[sys.argv.index('-C')+1:]))

elif 'run' in sys.argv:
  main('file', sys.argv[sys.argv.index('run')+1])

else:
  main('repl')

