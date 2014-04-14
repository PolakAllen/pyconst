import functools as ft

"""
Ultra Broken. 
We need a good way to intercept the base decorator, and modify decorator
functions. Other than, you know, the essential details, should provide a
metadata framework for generic decorators

Oh screw it. Just make my decorators conform to their own specification

Warning, mind melting levels of metas ensue
Currently intended for function decorators only
Non-wrapping decorators are ignored
Turns decorators into pure metadata. Performance unproven, though it does
provide tail recursion in decorators.

These are meta decorators intended for meta decorators
However, most are applicable to normal decorators

Save our annotations to a special __field__
Allows for a meta-meta-decorator that can possibly
interweave the annotations to reduce the overhead (dynamic mixin)
This allows us to easily ignore out decorators for the purpose of getting
the base or non-namespace decorated function function.

For that matter, we can likely also get parent decorators by examining the call
stack.
"""

class DecoratorProbe:
  """
  A proxy decorator.
  When created 
    insert self as bottom decorator, if we're not already there
    otherwise, do nothing (passthrough)
  When called, 
    analyses all called decorators
    stores them into metadata
    calls the original function
    replace entire decorator stack with desired function
    return result
  """
  def __init__(self, spot_in_decorator_block, replacement_function):
    self.newfn = replacement_function
    base = spot_in_decorator_block
    while hasattr(base,"__wrapped__"):
      base = base.__wrapped__
      base.__code__ = #TODO
    return 
     
  def __call__(self, args*, kwargs**):
    #TODO

def _meta_meta(wrapped_decorator, namespace="__decorators__", order=None):
  "We wrap a decorator, and assume only 1 metadecorator"

  #TODO: probably not going to work without uber hacks
  #       we need to intercept the definition of the __closure__ object that is
  #       contained in the definition object. Maybe we could re-write the
  #       function, but we risk modifying the behavior of other things
  #       anyways, not something I want to deal with right now
  def ultrawrap(base, decorators):
    """
    Order decorators
    We flatten the namespace decorations, so that decorators are not on the
    callstack.
    """
    if order: decorators = order(decorators)
    setattr(base, namespace, decorators)
    for decorator in decorators:
      #TODO

    wrapped = annotation
    if not namespace in annotation
      setattr(annotation, namesapce, [])
      wrapped = #TODO
    space = getattr(annotation, namespace)
    space.append(meta)

meta_mixin = ft.partial(_meta_meta, "__mixin__")
