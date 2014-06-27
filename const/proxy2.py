from const.mode import *
from aptools.magicnames import magicnames
import natures
import functools as ft
"""
Proxy can be initiated on a per-class or per-attribute/function level

At the class level, Proxy will simply return a pure ProxyClass. The ProxyClass
has the same __mro__ as the proxied class, but does not call any super methods,
delegating the construction of the object to the overriden class

At the method level, Proxy can do a few things:
  pass ProxyClass(self) instead of self
  pass additional proxy targets at invokation
  wrap the return value

At the attribute level, Proxy can do similar things as the method level, due to
descriptors. We wrap any existing descriptors, and (given that descriptors take
no arguments) we can return the attribute wrapped in a proxy.
"""

for name,val in shortnames.items():
  globals()[name] = val


class ProxyClassFactory:
  """
  A Base class for proxy class factories

  Proxies are meant to be transparent wrappers to a proxied object.
  To be more efficient, proxy classes are made per proxied object class.
  This is because there are many __ methods which cannot be dynamically proxied,
  and most be found in the class definition.

  Non-__ methods are proxied dynamically, as normal

  We abuse descriptors here. All autoproxied elements use a descriptor attribute
  (if its not callable). Otherwise it delegates to the method directly

  This creates some interesting issues. noautoproxy is a blacklist of attributes
  which should not be proxied as it causes catastrophic failure

  The only reliable way to differentiate the Proxied class is to test for a
  __proxy__ attribute, which is a local namespace for storing proxy data
  """
  noautoproxy = {"__dict__", "__class__", "__init__", "__qualname__", "__flags__",
    "__bases__","__name__", "__mro__", "__setattr__","__getattribute__",
    "__getattr__", "__new__"}

  def __init__(factory):
    factory.class_cache = {}

  def proxy_attr(factory, proxy, proxied, attrname):
    @property
    def autoproxyattr(self):
      return _get(d_geti(_get(self,"__proxy__"),"obj"), attrname)
    setattr(proxy, attrname, autoproxyattr)

  def proxy_method(factory, proxy, proxied, methodname):
    def autoproxymethod(self, *args, **kwargs):
      return _get(d_geti(_get(self,"__proxy__"),"obj"), methodname)(*args, **kwargs)
    setattr(proxy, methodname, autoproxymethod)

  def proxy(factory, proxy, proxied, name):
    attr = getattr(proxied, name)
    if callable(attr):
      factory.proxy_method(proxy, proxied, name)
    else:
      factory.proxy_attr(proxy, proxied, name)

  def build_class(factory, proxied_class):
    try:
      return factory.class_cache[proxied_class]
    except KeyError:
      class Proxy:
        def __init__(self, *args, **kwargs):
          metadata = {}
          metadata["obj"] = proxied_class(*args, **kwargs)
          setattr(self, "__proxy__", metadata)

        @property
        def __dict__(self):
          return _get(d_geti(_get(self,"__proxy__"),"obj"),"__dict__")
        @property
        def __class__(self):
          return _get(d_geti(_get(self,"__proxy__"),"obj"),"__class__")
        def __getattribute__(self, item):
          return _get(d_geti(_get(self,"__proxy__"),"obj"),item)

      for name in set(proxied_class.__dict__) - factory.noautoproxy:
        factory.proxy(Proxy, proxied_class, name)
      for name in set(magicnames) - factory.noautoproxy:
        if hasattr(proxied_class, name):
          factory.proxy(Proxy, proxied_class, name)

      factory.class_cache[proxied_class] = Proxy
      return Proxy

def infectious(CRTP):
  class InfectiousProxy(ProxyClassFactory, CRTP):
    def proxy_attr(factory, proxy, proxied, attrname):
      print("proxying",attrname,"as property")
      @property
      def autoproxyattr(self):
        return getattr(self.__proxy__["obj"], attrname)
      setattr(proxy, attrname, autoproxyattr)

    def proxy_method(factory, proxy, proxied, methodname):
      print("proxying",methodname,"as method")
      def do_method(self, obj, *args, **kwargs):
        getattr(obj, methodname)
        
      def autoproxymethod(self):
        obj = self.__proxy__["obj"]
        return ft.partial(do_method, self, obj)

      #autoproxymethod.__get__ = do_method
      setattr(proxy, methodname, autoproxymethod)
  return InfectiousProxy

@infectious
class Immutable:
  def Get(factory, *args): 
    print("Getting", *args)
    return FunctionNature.SafeNone
  def Modify(factory, *args): raise TypeError("class is immutable")
  def Set(factory, *args): raise TypeError("class is immutable")

immutable = Immutable().build_class
def nomutate(fn_or_target, *targets):
  def nomutate_inner(fn, targets=[]):
    def do_fn(*args, **kwargs):
      # bind the names to the arguments
      # wrap targeted arguments
      # marshal arguments to function in same manner as passed originally
      pass
    return do_fn

  if not isinstance(fn_or_target, target.Target):
    return nomutate_inner(fn)
  else: 
    return ft.partial(nomutate_inner, targets=[fn_or_target] + targets)

@immutable
class Test:
  a = 1
  def __init__(self):
    self.b = 2
    self.l = []
