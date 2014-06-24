from const.mode import *
from aptools.magicnames import magicnames
import functools as ft

for name,val in shortnames.items():
  globals()[name] = val

class ProxyClassFactoryFactory:
  """
  A Base class for proxy class factories

  Use:
    Create an instance of ProxyClassFactoryFactory. This initialization allows
    use of arbitrary natures in subclassing


  """
  # note that __class__ of Proxy will != proxied object class, though Proxy will
  # still be considered instanceof(Proxy, cls)
  providednames = [ "__init__", "__class__"]
  autoproxiednames = [ "__qualname__", "__name__", "__bases__", "__mro__", 
      "__flags__", "__module__"
  ]

  @Modeless
  def __init__(self, **kwargs):
    extra = set(kwargs) - {cls.__name__ for cls in FunctionNature.natures}
    if extra: raise TypeError("{} are invalid parameters".format(extra))

    self.intercepts = { cls:( wrap(kwargs[cls.__name__]) if cls.__name__ in kwargs 
                           else lambda *_, **__: FunctionNature.SafeNone ) 
                     for cls in FunctionNature.natures }

  def method_self_proxy(self):
    return o_get(self, "obj") #base class do nothing

  def get_cls_attr_proxy(self, cls, methodname):
    return getattr(cls, methodname)

  def get_generic_method_proxy(self, cls, methodname):
    method = getattr(cls, methodname)
    @ft.wraps(method)
    def inner(self, *args, **kwargs):
      obj = o_get(self, "method_self_proxy")()
      # we use the dictionary object to get the function, as we may want to pass
      # a self proxy to the function
      return method(obj, *args, **kwargs)
    return inner

  def get_autoproxied_method_proxy(self, cls, methodname):
    return getattr(cls, methodname)

  @Modeless
  def get_proxy_class(self, cls):
    # WARNING: note the usage of o_get and o_set vs getattr, setattr
    # these are hints to where a given block is being executed
    # o_* is used after Proxy class creation, to prevent accidental infinite
    # recursion in an object access
    if cls in self.cache:
      return self.cache[cls]

    Proxy = type(cls.__name__, (object,), {})
    def init(self, *args, **kwargs): 
      o_set(self, "obj", cls(*args, **kwargs))
    setattr(Proxy, "__init__", init)

    for type_, attrs in c_level_overrides.items():
      if issubclass(cls, type_):
        for method, nature in attrs.items():
          setattr(Proxy, method, nature.make(nature, self.intercepts[nature]))

    for name in autoproxiednames:
      if hasattr(cls, name):
        setattr(Proxy,name,getattr(cls, name))

    for method in magicnames:
      if method not in providednames and method not in autoproxiednames:
        try:
          attr = getattr(parent_class, method)
        except: continue

        if callable(attr):
          attr = self.method_proxy(attr)

        try:
          print("setting",method)
          setattr(Proxy, method, attr)
        except:
          raise TypeError("Invalid property " + method)
    self.cache[cls] = Proxy
    return Proxy

class InfectiousProxy(ProxyDispatch):

    
  @Modeless
  def __init__(self, **kwargs):
    super().__init__(derived)


""" Obsolete
    # The basic methods
    def __getattr__(self, attr):
      obj = o_get(self, "obj")
      val = o_get(obj, attr)
      val = on_get(obj, "__getattr__", attr, val)
      return Proxy(val)

    def __setattr__(self, attr, val):
      obj = o_get(self, "obj")
      o_set(obj, attr, on_set(obj, "__setattr__", attr, val))

    def __delattr__(self, attr):
      obj = object_nomode_getattribute(self, "obj")
      if on_del(obj, "__delattr__", attr):
        object_nomode_delattr(obj, attr)

    # list + dict, getters and setters
    def __setitem__(self, item, val):
      obj = _get(self, "obj")
      on_set(obj, "__setitem__", item, val)
    def __delitem__(self, item):
      obj = _get(self, "obj")
      # on_del must delete the item
      on_del(obj, "__delitem__", item)
    def __getitem__(self, item):
      obj = object_nomode_getattribute(self, "obj")
      getitem = object_nomode_getattribute(obj, "__getitem__")
      val = getitem(item)
      on_get(obj, "__getitem__", item, val)
      return Proxy(val)
    def __call__(self, *args, **kwargs):
      obj = object_nomode_getattribute(self, "obj")
      result = obj(*args, **kwargs)
      return Proxy(result)
    def append(self, item):
      obj = _get(self, "obj")
      on_set(obj, "append", None, item)
    def clear(self):
      obj = _get(self, "obj")
      # on_del must clear the list
      on_del(obj, "clear", None)
"""
