from forbidden.mode2 import *
from functools import wraps

def on_instance(cls, do):
  old_init = cls.__init__
  @wraps(old_init)
  def new_init(self, *args, **kwargs):
    print("new init",self)
    old_init(self, *args, **kwargs)
    do(self)
  cls.__init__ = new_init

def immutable(target):
  def set_noassign(instance):
    def noassign(obj, attr, val):
      raise AssertionError("Object is immutable")
    setmeta(instance, SET_ATTR, noassign)
    print("setmeta noassign on instance", instance)
  on_instance(target, set_noassign)
  return target

@immutable
class Test:
  def __init__(self):
    self.assign()

  def assign(self):
    self.t = []

  def mutate(self):
    self.t.append(1)

  def delete(self):
    del self.t
