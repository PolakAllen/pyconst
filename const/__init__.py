from const.mode import *
import const.proxy
from const.target import Target as Params
from functools import wraps
import types

def on_instance(do):
  def do_on_instance(cls):
    old_init = cls.__init__
    @wraps(old_init)
    def new_init(self, *args, **kwargs):
      old_init(self, *args, **kwargs)
      do(self)
    cls.__init__ = new_init
    return cls
  return do_on_instance


def no_set(*_):
  raise AssertionError("Object is const")

def immutable(cls):
  proxy_class = const.proxy.build( cls, on_set=no_set, on_del=no_set )
  return proxy_class

def modifies(target):
  return lambda _: _
