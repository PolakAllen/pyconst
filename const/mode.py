from const.meta import *
from const.natures import *

GET_ATTRIBUTE = next(Metadata)
SET_ATTR = next(Metadata)
DEL_ATTR = next(Metadata)

def object_getattribute(obj, attr):
  # first check the stack mode
  if metastate() == MODE_LESS:
    # keeps things from getting ugly (random infinite recursion sound like fun?)
    # *note: getmeta may not be recursion safe
    # requires a __getattribute__ check for __hash__ (with dict[])
    return object_nomode_getattribute(obj, attr)
  try:
    # objmode might return object_nomode_getattribute, or a proxy value
    objmode = getmeta(obj, GET_ATTRIBUTE)
  except AttributeError: pass
  else:
    if objmode: return objmode(obj, attr)
  return object_nomode_getattribute(obj, attr)

def object_setattr(obj, attr, val):
  if metastate() == MODE_LESS:
    return object_nomode_setattr(obj, attr, val)
  try:
    # objmode might use object_nomode_setattr, or it might assign to a proxy
    objmode = getmeta(obj, SET_ATTR)
  except AttributeError: pass
  else:
    if objmode: return objmode(obj, attr, val)
  return object_nomode_setattr(obj, attr, val)

def object_delattr(obj, attr):
  if metastate() == MODE_LESS:
    return object_nomode_delattr(obj, attr)
  try:
    objmode = getmeta(obj, DEL_ATTR)
  except AttributeError: pass
  else:
    if objmode: return objmode(obj, attr)
  return object_nomode_delattr(obj, attr)
    
curse(object, "__getattribute__", object_getattribute)
curse(object, "__setattr__", object_setattr)
curse(object, "__delattr__", object_delattr)

