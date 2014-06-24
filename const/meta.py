from forbiddenfruit import curse
from threading import current_thread
from itertools import count

Metadata = count(1)
MODE_LESS = next(Metadata)

def push_metastack(val):
  t = current_thread()
  try:
    list_nomode_append(object_nomode_getattribute(t,"__metastack__"),val)
  except AttributeError:
    object_nomode_setattr(t,"__metastack__",[])
    return push_metastack(val)

def pop_metastack():
  t = current_thread()
  try:
    list_nomode_pop(object_nomode_getattribute(t,"__metastack__"))
  except (AttributeError, IndexError):
    raise AssertionError("Invalid program state. Metastack popped more times than pushed")

def metastate():
  t = current_thread()
  try:
    return list_nomode_getitem(object_nomode_getattribute(t,"__metastack__"),-1)
  except AttributeError:
    object_nomode_setattr(t,"__metastack__",[])
    return metastate()
  except IndexError:
    return None

def Modeless(fn):
  def modeless_fn(*args, **kwargs):
    push_metastack(MODE_LESS) 
    try:
      return fn(*args, **kwargs)
    finally:
      pop_metastack()
  return modeless_fn

@Modeless
def setmeta(obj,attr,val,target=None):
  if target is None:
    return obj.__setmeta__(attr, val)
  else:
    return obj.__setmeta__(target, attr, val)

@Modeless
def getmeta(obj,attr,default=None,target=None):
  try:
    if target is None:
      return obj.__getmeta__(attr)
    else:
      return obj.__getmeta__(target, attr)
  except KeyError:
    return default

@Modeless
def delmeta(obj,attr,target=None):
  if target is None:
    return obj.__delmeta__(attr)
  else:
    return obj.__delmeta__(target, attr)

# __metadata__ is a global slot, so we have to manage the namespaces
curse(object, "__metadata__", {})
def _get(namespace,obj):
  try:
    return namespace[id(obj)]
  except KeyError:
    namespace[id(obj)] = {}
    return namespace[id(obj)]
    
@Modeless
def _object_getmeta(obj,attr):
  return _get(object.__metadata__, obj).get(attr)

@Modeless
def _object_setmeta(obj,attr,val):
  _get(object.__metadata__, obj)[attr] = val

@Modeless
def _object_delmeta(obj,attr):
  del _get(object.__metadata__, obj)[attr]

curse(object, "__getmeta__", _object_getmeta)
curse(object, "__setmeta__", _object_setmeta)
curse(object, "__delmeta__", _object_delmeta)
