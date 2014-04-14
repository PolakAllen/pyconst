#!/usr/bin/python3
import os
import fnmatch
import metadata

# Project specific settings


###############################################################################
"""
From Don't Ever Do This In Python
import marshal
import test_project
print(test_project.__cached__)
with open(test_project.__cached__, 'rb') as f:
  code = marshal.loads(f.read()[12:])
f.__code__ = code
f()

class PyFile
"""

if __name__ == "__main__":
  print(__build_class__, __debug__, __doc__, __import__, __loader__, __name__, __package__, sep="\n")
  OBJECT_DIR = 'obj'
  SOURCE_DIR = 'src'
  # compiled files with compile times
  _compiled = {}
  for root, _, filenames in os.walk(OBJECT_DIR):
    for fname in filenames:
      _compiled[fname] = os.path.getctime(os.path.join(root,fname))

  # uncompiled files with last change times > compiled times
  _needs_compile = []
  for root, dirnames, filenames in os.walk(SOURCE_DIR):
    if filenames:
      for fname in fnmatch.filter(filenames, '*.py'):
        if fname not in _compiled or _compiled[filename] < os.path.getmtime(fname):
            _needs_compile.append(fname)

  if not _compiled and not _needs_compile:
    print("Empty project or project files not found")

  for fname in _needs_compile:
      oname =  os.path.join(OBJECT_DIR,os.path.splitext(fname)[0]) + ".pyc"
      with open(oname, 'w') as f:
          print("Compiling: ",fname,oname)
          f.write(metadata.compiler.compile(fname))
  else:
      print("No compilation needed")

