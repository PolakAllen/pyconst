from forbiddenfruit import curse
"""
As we overwrite default methods in python, supreme clairity of thought is
required to understand this module

We have __metadata__ dictionaries on all python primatives
To successfull override __getattribute__ and __setattr__, we need successfully
  get data in and out of those dictionaries without using the builtin python
  __getattribute__ and __setattr__.

We have the problem of overwritting object,list,dict.__getattribute__ as well.
  We can't access the base method via the object anymore, as doing so will invoke
  the new __getattribute__ method.
  Not overwritting __getattribute__ will not the results we need, as sometimes
  we need to return a proxy object

Typically this would be best done as part of a C module. Unfortunately I don't
  have time to implement that right now

Method 1:
  Use stack frames as hints to check for object __metadata__
  Flaw: Cannot support nonstack modes, issues when nesting validations
Method 2:
  store flat proceedures for accessing __metadata__
  ensure this access order:
    object.attr 
      => object.__getattribute__(attr)
        => getmetadata(object,MODE)
        => getmetadata(frame,MODE)
        => object_nomode_getattribute(object,attr) # global method
  we'll only need flat proceedures for __getattribute__, but care must be taken
  so that we can access our proceedures (for dict at least) in a modeless manner
"""

def nomode_hasattr(Type):
  raw_fn = Type.__getattribute__
  def hasattr(obj, attr):
    try:
      raw_fn(obj, attr)
      return true
    except AttributeError:
      return false

#__builtins__["object_nomode_getattribute"] = object.__getattribute__
#__builtins__["list_nomode_getattribute"] = list.__getattribute__
#__builtins__["dict_nomode_getattribute"] = dict.__getattribute__
#__builtins__["object_nomode_hasattr"] = nomode_hasattr(object)
#__builtins__["dict_nomode_hasattr"] = nomode_hasattr(dict)
#__builtins__["list_nomode_hasattr"] = nomode_hasattr(list)
#__builtins__["list_nomode_getitem"] = list.__getitem__
#__builtins__["list_nomode_setitem"] = list.__setitem__
#__builtins__["dict_nomode_getitem"] = dict.__getitem__
#__builtins__["dict_nomode_setitem"] = dict.__setitem__

to_be_replaced = {
  object:["__getattribute__", "__setattr__", "__delattr__"],
  list:["__getattribute__", "__setattr__", "__delattr__", 
      "__getitem__", "__setitem__", "__delitem__", 
      "__contains__", "append", "clear", 
      "extend", "pop", "remove", "insert"],
  dict:["__getattribute__", "__setattr__", "__delattr__", 
      "__getitem__", "__setitem__", "__delitem__", 
      "__contains__", "get", "pop", "popitem", 
      "update", "setdefault"]
}
def transform_name(name):
  if name.startswith("__"):
    return "__nomode_" + name[2:]
  else:
    return "nomode_" + name

for obj, names in to_be_replaced.items():
  for name in names:
    transformed_name = transform_name(name)
    print("adding {} to {}".format(transformed_name, obj))
    curse(obj, transformed_name, getattr(obj, name))

def nomode_getattr(obj, attr, default=None):
  try:
    return object_nomode_getattribute(obj, attr)
  except AttributeError:
    try:
      return object_nomode_getattribute(obj, "__getattr__")(attr)
    except AttributeError:
      return default

__builtins__["object_nomode_getattr"] = nomode_getattr

def nomode_setattr(obj, attr, value):
  dict_nomode_setitem(object_nomode_getattribute(obj,"__dict__"),attr,value)

__builtins__["object_nomode_setattr"] = nomode_setattr


def freeze(obj):
  if isinstance(obj, dict):
    return tuple(sorted(obj.items()))
  if isinstance(obj, list):
    return tuple(obj)
  if isinstance(obj, object):
    return tuple(sorted(obj.__dict__.items()))

def setmeta(obj,attr,m):
  try:
    return object_nomode_getattribute(obj,"__setmeta__")(obj,attr,m)
  except AttributeError:
    def try_setmeta(obj):
      metadata = object_nomode_getattribute(obj,"__metadata__")
      if not obj in metadata:
        dict_nomode_setitem(metadata,obj,{})
      dict_nomode_setitem(dict_nomode_getitem(metadata,obj),attr,m)
    try_setmeta(obj)
    #try: 
    #except TypeError: try_setmeta(freeze(obj))

def getmeta(obj,attr,default=None):
  try:
    return object_nomode_getattribute(obj, "__getmeta__")(attr) or default
  except AttributeError:
    try:
      metadata = object_nomode_getattribute(obj, "__metadata__")
    except: pass
    else:
      try:
        objmetadata = dict_nomode_getitem(metadata,obj)
      except TypeError:
        raise
        #objmetadata = nomode_getattribute(metadata,freeze(obj))
      finally:
        return dict_nomode_getitem(objmetadata,attr) if attr else objmetadata
    finally: # if we haven't returned so far
      return default

def delmeta(obj):
  try:
    return object_nomode_getattr(obj,"__delmeta__")(obj)
  except AttributeError:
    metadata = object_nomode_getattr(obj, "__metadata__") 
    if obj in metadata:
      del obj[obj]

def bindmeta(obj, getmeta=None, setmeta=None, delmeta=None):
  curse(obj, "__metadata__", {})
  if getmeta: curse(obj, "__getmeta__", getmeta)
  if setmeta: curse(obj, "__setmeta__", setmeta)
  if delmeta: curse(obj, "__delmeta__", delmeta)

supported_types = [object, list, dict]
for t in supported_types:
  bindmeta(t)
