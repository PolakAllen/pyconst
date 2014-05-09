import decorator
import types
import weakref
from metadata.contractassert import *

def Functional(decorator): #future: fields=False, live=False
  """
  A powerful meta-decorator
  takes fn and creates safely wrapped version of original
  also will apply given decorator to a function, or to each member function
  
  future: live means dynamically adding the the class ensures that the new 
  function is wrapped as well
  """
  def wrapper(obj):
    if type(obj) is types.FunctionType:
      return decorator(obj)
    if type(obj) is type:
      for k,v in obj.__dict__.items():
        if type(v) is types.FunctionType:
          obj.__dict__[o] = decorator(obj.__dict__[o])
      return obj 
  return wrapper

def DynamicContract(decorator):
  """
  A meta-decorator
  contract decorators add themselves to the object in question,
  to be validated later by @Assert
  """
  def contract(obj):
    base = obj
    if not hasattr(obj,"__decoratorbase__"):
      setattr(obj, "__decoratorbase__", obj)
    else:
      obj = obj.__decoratorbase__
    if not hasattr(obj, "__contracts__"):
      setattr(obj, "__contracts__", [])
    if not decorator in obj.__contracts__:
      obj.__contracts__.append(decorator)
    return DynamicAssert(obj)
  return contract


