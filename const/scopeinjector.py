import sys
import inspect

class base_injector:
  def __setattr__(self,name,value): 
    self.scope[name] = value 
  def __setitem__(self,name,value):
    self.scope[name] = value

class global_injector(base_injector):
  def __init__(self): 
    try: 
      self.__dict__['scope'] = sys.modules['__builtin__'].__dict__ 
    except KeyError: 
      self.__dict__['scope'] = sys.modules['builtins'].__dict__ 

Globals = global_injector()
