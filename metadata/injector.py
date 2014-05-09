from metadata.contract import DynamicContract
from decorator import decorator
import types

passes = ["__{}__".format(name) for name in 
    ["str","repr","sizeof","subclasshook","reduce","reduce_ex",
    "ne","eq","le","lt","ge","gt","hash", "dir", "format",
    "module","doc"]]

def injector(obj, name):
  unknown = object.__getattribute__(obj, name)

def injectionfactory(name, Wrapper):
  def autowrap(self, *args, **kwargs):
    innerobj = object.__getattribute__(self,"obj")
    fn = object.__getattribute__(innerobj, name)
    result = fn(*args, **kwargs)
    return Wrapper(result)

def passthroughfactory(name):
  def autowrap(self, *args, **kwargs):
    print("accessing {}".format(name))
    innerobj = object.__getattribute__(self,"obj")
    fn = object.__getattribute__(innerobj, name)
    print("fn found is {}".format(fn))
    result = fn(*args, **kwargs)
    return result
  return autowrap
  
def sentinalwrap(setter, cls):
  class SentinalWrapper:
    # we have a basic set of methods
    def __init__(self, *args, **kwargs):
      obj = cls(*args, **kwargs)
      object.__setattr__(self, "obj", obj)
    def __getattribute__(self, item):
      """cache management"""
      obj = object.__getattribute__(self,"obj")
      unknown = object.__getattribute__(obj,item)
      if unknown is types.FunctionType:
        injectionfactoryunknown

  SentinalWrapper.__setattr__ = setter
  return SentinalWrapper

def sentinal(cls, setter):
  return sentinalwrap(setter,cls)
  """
  if isinstance(value, list):
    for i in value:
      i = sentinal(i, setter)
    value.__setattr__ = setter
    return value
  if isinstance(value, tuple):
    newvalue = []
    for i in value:
      newvalue.append(sentinal(i, setter))
    newvalue.__setattr__ = setter
    return newvalue
  if isinstance(value, dict):
    for k in value:
      value[k] = sentinal(value[k], setter)
    value.__setattr__ = setter
    return value
  if isinstance(value, (types.GetSetDescriptorType, types.BuiltinMethodType,
      types.MemberDescriptorType)):
    # do nothing, they're immutable anyways
    return value
  if hasattr(value, "__dict__"):
    for v,k in value.__dict__.items():
      value[k] = sentinal(v, setter)
    value.__setattr__ = setter
    return value
  return sentinalwrap(setter)(value)
  """
