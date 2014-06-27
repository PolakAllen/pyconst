from aptools.magicnames import magicnames

def autoproxy(proxy, cls, name):
  def autoproxyattr_factory(attrname):
    @property
    def autoproxyattr(self):
      return getattr(self.__metadata__["obj"], attrname)
    return autoproxyattr
  def autoproxymethod_factory(methodname):
    def autoproxymethod(self, *args, **kwargs):
      return getattr(self.__metadata__["obj"], methodname)(*args, **kwargs)
    return autoproxymethod
  attr = getattr(cls, name)
  if callable(attr):
    setattr(proxy, name, autoproxymethod_factory(name))
  else:
    setattr(proxy, name, autoproxyattr_factory(name))

def ProxyWrap(proxied_class):
  class Proxy:
    def __init__(self, *args, **kwargs):
      self.__metadata__ = {}
      self.__metadata__["obj"] = proxied_class(*args, **kwargs)

    @property
    def __dict__(self):
      return self.__metadata__["obj"].__dict__
    @property
    def __class__(self):
      return self.__metadata__["obj"].__class__
  #TODO: no idea what __flags__ are
  # need to check what the implications are for not using __new__
  noproxy = {"__dict__", "__class__", "__init__", "__qualname__", "__flags__",
    "__bases__","__name__", "__mro__", "__setattr__","__getattribute__","__new__"}

  for name in set(proxied_class.__dict__) - noproxy:
    print("proxying",name)
    autoproxy(Proxy, proxied_class, name)
  for name in set(magicnames) - noproxy:
    if hasattr(proxied_class, name):
      print("proxying", name)
      autoproxy(Proxy, proxied_class, name)
  return Proxy
  

@ProxyWrap
class Proxied(list):
  def __init__(self, l):
    self[:] = l
