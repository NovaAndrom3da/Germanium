import os, sys, subprocess

def clear():
  print('\x1b[2J')

def singlefile():
  files = {}
  imports = []
  order = [
    'typing.py',
    'errors.py',
    'funcs.py',
    'lexer.py',
    '__init__.py'
  ]
  
  for file in order:
    if os.path.isfile('src/'+file):
      f = open('src/'+file)
      content = f.read().replace(',\n  ', ',').replace('[\n', '[')\
        .replace('\n]', ']').replace('{\n','{').replace('\n}','}')
      f.close()
      o = []
      for line in content.split('\n'):
        nospace = line.replace(' ','')
        if nospace.startswith('#') or nospace == '':
          pass
        elif line.startswith('from .'):
          pass
        elif line.startswith('import '):
          for i in line[6:].split(','):
            imports.append(i.lstrip(' ').rstrip(' '))
        else:
          o.append(line)
      files[file] = '\n'.join(o)
    else:
      print(f"'{file}' is not a file")
  
  imports_out = []
  for i in imports:
    if not i in imports_out:
      imports_out.append(i)
  out = f"import {','.join(imports_out)}\n"
  for f in files.keys():
    out += files[f] + '\n'
  return out

def build():
  try:
    os.mkdir('build')
  except FileExistsError:
    print("[Error] 'build' folder already exists")
    sys.exit()
  outfile = open('build/Germanium.py', 'w')
  outfile.write(singlefile())
  outfile.close()

  # compile stuff here or smth

def install_src():
  build()

def bin_output_files(l=[], data=b''):
  for i in l:
    nf = open('bin/'+i, 'wb')
    nf.write(data)
    nf.close()
    os.chmod('bin/'+i, 777)

def prompt():
  return input('? ').lower().lstrip(' ').rstrip(' ')[0]

def install_build():
  build()
  print('[n] Build with Nuitka')

  i = prompt()
  if i == 'n':
    os.chdir('build')
    p = subprocess.Popen(('python3', '-m', 'nuitka', '--follow-imports', 'Germanium.py'))
    p.communicate()
    os.chdir('..')
    os.mkdir('bin')
    bin_data = b''
    if 'Germanium.bin' in os.listdir('build'):
      of = open('build/Germanium.bin', 'rb')
      bin_data = of.read()
      of.close()
      os.remove('build/Germanium.bin')
    
    bin_output_files(['germanium', 'ge'], bin_data)
    
    cleanup()

def cleanup():
  os.remove('build/Germanium.py')
  

def main():
  try:
    loop = True
    while loop:
      clear()
      print('[s] Install Germanium (Source)')
      print('[c] Install Germanium (Compiled)')
      print('[r] Run Germanium (Source)')
      
      i = prompt()
      if i == 's':
        loop = False
        install_src()
      elif i == 'c':
        loop = False
        clear()
        install_build()
      elif i == 'r':
        loop = False
        clear()
        exec(singlefile())
      else:
        pass
  except Exception as e:
    print(f"Something happened:\n{str(e)}\nExiting.")

main()