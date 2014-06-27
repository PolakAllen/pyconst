from aptools.scopeinjector import Globals
from aptools.objectdict import ObjectDict

class FunctionNature:
  # SafeNone should be returned if an intercept function doesn't want to be have
  # it's result considered (no intercept)
  SafeNone = type("Nill", (object,), {})()
  class Nature:
    """builds a composite function from the client, based on the specific Nature"""
    def __init__(nature, base_fn):
      nature.base_fn = base_fn

    def make(nature, intercept_fn):
      def composite(*args, **kwargs):
        intercept_result = intercept_fn(nature.base_fn, args, kwargs)
        return nature.handle(intercept_result, args, kwargs)
      return composite

    def handle(self, result, args, kwargs):
      return self.base_fn(*args, **kwargs) if FunctionNature.SafeNone == result else result

  class Get(Nature): modifies = False
  class Set(Nature): modifies = True
  class Del(Nature): modifies = True
  class Modify(Nature): modifies = True
  class Iter(Nature): modifies = False
  natures = [Get, Set, Del, Modify, Iter]

c_level_overrides = {
    object:{
      "__getattribute__":FunctionNature.Get,
      "__setattr__":FunctionNature.Set,
      "__delattr__":FunctionNature.Del,
    },
    list:{
      "__getitem__":FunctionNature.Get,
      "__setitem__":FunctionNature.Set,
      "__delitem__":FunctionNature.Modify,
      "append":FunctionNature.Set,
      "insert":FunctionNature.Modify,
      "remove":FunctionNature.Modify,
      "clear":FunctionNature.Modify,
      "pop":FunctionNature.Del,
      "sort":FunctionNature.Modify,
    },
    dict:{
      "__getitem__":FunctionNature.Get,
      "__setitem__":FunctionNature.Set,
      "__delitem__":FunctionNature.Del,
      "get":FunctionNature.Get,
      "pop":FunctionNature.Del,
      "clear":FunctionNature.Modify,
      "update":FunctionNature.Modify,
      "popitem":FunctionNature.Del,
    },
    set:{
      "add":FunctionNature.Set,
      "pop":FunctionNature.Del,
      "remove":FunctionNature.Del,
      "update":FunctionNature.Modify,
      "discard":FunctionNature.Del,
    }
}
Globals.shortnames = { 
    object:"", list:"l", dict:"d", set:"s",
    "__getattribute__":"get", "__getitem__":"geti",
    "__setattr__":"set", "__setitem__":"seti",
    "__delattr__":"del", "__delitem__":"deli" }
Globals.nomode = ObjectDict(
    **{ type_.__name__:ObjectDict(
        **{ fnname:getattr(type_,fnname) for fnname in attrs })
      for type_,attrs in c_level_overrides.items() 
    })

for obj,fns in c_level_overrides.items():
  for method,nature in fns.items():
    methodfullname = "_".join([obj.__name__,"nomode",method.strip('_').rstrip('_')])
    methodshortname = "_".join([shortnames[obj],shortnames.get(method,method)])
    fn = getattr(obj, method)
    Globals[methodfullname] = shortnames[methodshortname] = fn
    # patch overrides to include the base function programmatically
    c_level_overrides[obj][method] = nature(fn) 

