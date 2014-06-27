from const.natures import c_level_overrides, FunctionNature
from const.magicnames import magicnames

safe_primatives = { str, int, float, complex }
class ProxyMetadata:
  def __init__(self, obj, proxy_type, context=None):
    self.obj = obj
    self.proxy_type = proxy_type
    self.context = context if context else [(obj,None,tuple(),{})]

  def __call__(self, value, new_context):
    return self.proxy_type(value, self.proxy_type, 
        self.context + [(value,) + new_context])
do_override = {"__str__","__repr__"}
class BaseProxy:
  def __init__(self, obj, proxy_type, context=None):
    self.__dict__["__proxy__"] = ProxyMetadata(obj, proxy_type, context)
    for name in set(magicnames) - (set(dir(proxy_type)) - do_override):
      if hasattr(obj, name):
        object.__setattr__(self, name, getattr(obj, name))


  @property
  def __class__(self):
    return self.__proxy__.obj.__class__

  def __getattribute__(self, item):
    try:
      return object.__getattribute__(self, item)
    except AttributeError: 
      proxy = object.__getattribute__(self,"__proxy__")
      value = getattr(proxy.obj, item)
      if type(value) in safe_primatives: return value
      return proxy(value, (getattr, (proxy.obj, item), {}))

  def __getitem__(self, item):
    proxy = object.__getattribute__(self,"__proxy__")
    value = proxy.obj.__getitem__(item)
    if type(value) in safe_primatives: return value
    return proxy(value, (proxy.obj.__getitem__, (item,), {}))

  def __iter__(self):
    proxy = object.__getattribute__(self,"__proxy__")
    for count,i in enumerate(proxy.obj.__iter__()):
      yield proxy(i, (proxy.obj.__iter__, (count,), {}))

  def __call__(self, *args, **kwargs):
    proxy = object.__getattribute__(self,"__proxy__")
    if hasattr(proxy.obj,"__self__"):
      parent = proxy.context[-2][0]
      fn_name = proxy.obj.__name__
      parent_proxy = proxy(parent, ("__call__",args,kwargs))
      fn = getattr(parent.__class__,fn_name)
      return fn(parent_proxy, *args, **kwargs)
    return proxy.obj(*args, **kwargs)
  def __repr__(self):
    proxy = object.__getattribute__(self,"__proxy__")
    return proxy.obj.__repr__()

def proxy_class(SpecializedProxy):
  def decorator(proxied_cls):
    class Proxy(SpecializedProxy):
      def __init__(self, *args, **kwargs):
        super().__init__(proxied_cls(*args, **kwargs), SpecializedProxy)
    return Proxy
  decorator.__inner__ = SpecializedProxy
  return decorator

def mutation_denied(self, *args, **kwargs): 
  raise TypeError("{} is immutable in this instance".format(self.__class__.__name__))

@proxy_class
class Immutable(BaseProxy):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

for objtype, methods in c_level_overrides.items():
  for method, nature in methods.items():
    if nature.modifies:
      setattr(Immutable.__inner__, method, mutation_denied)

def proxy(factory, proxy, proxied, name):
  attr = getattr(proxied, name)
  if callable(attr):
    factory.proxy_method(proxy, proxied, name)
  else:
    factory.proxy_attr(proxy, proxied, name)
  
  

def nomutate(field):
  return Immutable.__inner__(field, Immutable.__inner__)

@Immutable
class Test:
  a = []
  def __init__(self):
    self.b = []
  def mutateb(self):
    self.b.append(1)

class Test2:
  a = []
  def __init__(self):
    self.b = []
    self.c = nomutate([1,2,3])
