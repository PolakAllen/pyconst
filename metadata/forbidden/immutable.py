from forbidden.mode import Validation
from forbidden.target import Target
from forbidden.meta import setmeta
from forbidden.mode import MODE
import functools as ft
self = Target(attr="self")

class nomodify(Validation):
  def setattr(self, obj, attr, val):
    raise ValueError("No Setting Allowed!")

class noassign(Validation):
  def __init__(self, attr):
    self.attr = attr

  def getattr(self, obj, attr):
    val = Proxy(nomodify(nomode_getattr(obj, attr)))
    print("setting nomutate on",attr,val)
    setmeta(val, MODE, nomodify())
    return val

  def setattr(self, obj, attr, val):
    if self.attr == attr:
      raise ValueError("No setting {} on {}".format(attr, obj))
    return False

class nomutate(Validation):
  def setattr(self, obj, attr, val):
    raise ValueError("No Setting Allowed!")

  def bind_parent(self, parent, attr):
    setmeta(parent, MODE, noassign(attr))
    
  def unbind_parent(self, parent, attr):
    setmeta(parent, MODE, None)
    
class Inner:
  def __init__(self):
    self.x = 0

class Test:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.inner = Inner()

  @nomutate(self)
  def mutateinner1(self):
    i = self.inner.x
    self.inner.x = i + 1
    return self.inner.x

  @nomutate(self.y)
  def mutatesx(self):
    self.x = self.x + 1
    return self.x

  @nomutate(self.inner)
  def mutateinner2(self):
    i = self.inner.x
    self.inner.x = i + 1
    return self.inner.x

  def unguarded(self):
    self.x += 1
    return self.x

def test():
  for t in [t1, t2, t3, t4]:
    t()

def t1():
  try:
    Test().mutateinner1()
    raise AssertionError("mutateinner1 should raise ValueError")
  except ValueError: pass

def t2():
  try:
    Test().mutateinner2()
    raise AssertionError("mutateinner2 should raise ValueError")
  except ValueError: pass

def t3():
  Test().mutatesx()

def t4():
  Test().unguarded()
