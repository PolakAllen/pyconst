from forbiddenfruit import curse
import functools as ft
import inspect
import types
from frame import frame
from forbidden.target import Target
from meta import *

"""
Creates modal operations on the python stack.
Mode is determined by metadata on the stack, and the object being accessed

Its expected that modes are primarly non-functionality, and silently validate.
Proxy mode is used if any active mode requires its use.
Proper handling of the exit of proxy mode is to be handled by other code
"""

"""Placeholder for future metadata definitions"""
MODE = 1
VALIDATIONS = 2
NO_VALIDATE_MODE = 3

"""
def mode(raw_name, access=None):
  print(raw_name)
  if not access:
    access = raw_name
  raw_fn_name = transform_name(access)
  def mode_attr(self, *args, **kwargs):
    try:
      objmode = nomode_getdictitem(getmeta(self, MODE, {}), access)
    except KeyError: objmode = None
    try:
      stackmode = nomode_getdictitem(getmeta(frame(0), MODE, {}), access)
    except KeyError: stackmode = None
    doproxy = False
    if objmode:   
      print("objmode",objmode)
      val = objmode(self, *args, **kwargs)
      if val:
        return val
    if stackmode: 
      print("stackmode",stackmode)
      val = stackmode(self, *args, **kwargs)
      if val:
        return val
    if doproxy:
      raise ValueError("Proxy mode unsupported")
    print("nomode_getattribute({}, {})".format(self, raw_fn_name))
    try:
      return __builtins__[raw_fn_name](self, *args, **kwargs)
    except:
      return nomode_getattribute(self, raw_fn_name)(*args, **kwargs)
  return mode_attr
"""

def getattribute(obj, attr):
  stackmode = getmeta(frame(0), MODE, {})
  setmeta(frame(0), MODE, NO_VALIDATE_MODE)
  if stackmode is NO_VALIDATE_MODE:
    return object_nomode_getattribute(obj, attr)

  try:
    objmode = dict_nomode_getitem(getmeta(obj, MODE, {}), "getattr")
  except KeyError: pass
  else:
    val = objmode(obj, attr)
    if val: return val
  return object_nomode_getattribute(obj, attr)

lookup = {(obj,name):val for obj,attrs in {
    object: {
        #"__setattr__":mode("__setattr__","setattr"),
        "__getattribute__":getattribute
        #"__delattr__":mode("__delattr__","delattr")
    }
  }.items() for name,val in attrs.items() 
}

for obj, names in to_be_replaced.items():
  for name in names:
    if (obj, name) in lookup:
      curse(obj, name, lookup[(obj, name)])
    else:
      print("WARNING: no specific handler for {} on {}".format(name, obj))

class AsObject(dict):
  def __init__(self, d):
    self.update(**d)
  def __getattr__(self, item):
    return self.__dict__.get(item, self[item])
class Proxy:
  def __init__(self, obj):
    self.obj = obj
  def __getattribute__(self, attr):
    return Proxy(getattr(nomode_getattribute(self,"obj"), attr))

class Validation:
  def __init__(self, *targets):
    object_nomode_setattr(self, "params", targets)

  def __getitem__(self, item):
    print("{} from validation {}".format(item,self.__class__.__name__))
    return getattr(self, item, None)
  def get(self, item, default=None):
    return self[item]
  def walk_fn(self, fn, args, kwargs):
    bound_args = inspect.signature(fn).bind_partial(*args, **kwargs)
    for target in self.params:
      n = AsObject(bound_args.arguments)
      prev = None
      attr = None
      for i,t in enumerate(target):
        name,args,kwargs = t
        if i > 0: 
          prev = n
          attr = name
        n = object_nomode_getattr(n, name)
        if args or kwargs:
          prev = n
          n = n(*args, **kwargs)
      yield prev, attr, n

  def bind_parent(self, parent, attr):
    pass
  def unbind_parent(self, parent, attr):
    pass

  def bind_targets(self, fn, args, kwargs):
    if self.params:
      for previous,attr,final in self.walk_fn(fn, args, kwargs):
        setmeta(final, MODE, self)
        self.bind_parent(previous, attr)
    else:
      setmeta(frame(1), MODE, self)

  def unbind_targets(self, fn, args, kwargs):
    if self.params:
      for previous,attr,final in self.walk_fn(fn, args, kwargs):
        setmeta(final, MODE, None)
        self.unbind_parent(previous, attr)
    else:
      setmeta(frame(1), MODE, None)
        
  def __call__(self, fn):
    @ft.wraps(fn)
    def call(*args, **kwargs):
      #self.bind_targets(fn, args, kwargs)
      rval = fn(*args, **kwargs)
      #self.unbind_targets(fn, args, kwargs)
      return rval
    return call
    
