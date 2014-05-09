from inspect import currentframe
import functools as ft
from meta import *

Frame = currentframe().__class__

def frame_getmeta(f_start,attr=None,default=None):
  f = f_start
  # until last frame, while our specific attribute or frame is not in __metadata__
  while( f and ( f not in object_nomode_getattribute(f,"__metadata__") or
                 ( attr and attr not in 
                   dict_nomode_getitem(
                       object_nomode_getattribute(f,"__metadata__"), f
                   )
                 )
               )
       ):
    f = object_nomode_getattribute(f,"f_back")
  if f:
    val = dict_nomode_getitem(object_nomode_getattribute(f,"__metadata__"), f)
    if attr:
      val = dict_nomode_getitem(val,attr)
    return val or default
  return default

bindmeta(Frame, getmeta=frame_getmeta)

def frameinfo(i):
  f = frame(i)
  return inspect.getframeinfo(f) + (getmeta(f),)

def frame(i):
  nextframe = currentframe()
  for i in range(i+1):
    nextframe = object_nomode_getattribute(nextframe,"f_back")
  return nextframe

