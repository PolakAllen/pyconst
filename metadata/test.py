import functools as ft
import decorator
import inspect

def passthrough(fn):
  @ft.wraps(fn)
  def ffn(*args, **kwargs):
    return fn(*args, **kwargs)
  return ffn

def decprints(fn):
  @decorator.decorator(fn)
  @ft.wraps(fn)
  def printer(*args, **kwargs):
    print(*args)
    return fn(*args, **kwargs)
  return printer

def ftprints(fn):
  @ft.wraps(fn)
  def printer(*args, **kwargs):
    print(*args)
    return fn(*args, **kwargs)
  return printer

def prints(fn):
  outter_var = "test"
  def printer(*args, **kwargs):
    print(*args)
    return fn(*args, **kwargs)
  setattr(printer,"__wrapped__",fn)
  return printer

def throws(fn):
  @ft.wraps(fn)
  def throw(*args, **kwargs):
    raise Exception
  return throw

def findclosure(dec):
  if hasattr(dec, "__closure__"):
    for o in dec.__closure__:
      print(dir(o.cell_contents))
      print(o.cell_contents.__name__)

def noop(*args, **kwargs):
  pass

def probe(dec):
  base = dec
  decorators = []
  while hasattr(base,"__wrapped__"):
    decorators.append((base.__name__, base.__code__))
    base.__code__ = noop.__code__
    base = base.__wrapped__
  setattr(base, "__decorators__", decorators)
  return base

@probe
@prints
def hello(name):
  print("Hello", name)

@probe
@ftprints
def helloft(name):
  print("Hello",name)

@probe
@decprints
def hellodec(name):
  print("Hello",name)
