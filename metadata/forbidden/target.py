"""
Dumb mock object for parameter targeting purposes
"""
class Target:
  def __init__(self, *args, attr=None, parent=None, **kwargs):
    self.__handle_metadata__ = {}
    self.__handle_metadata__["args"]   = args
    self.__handle_metadata__["kwargs"] = kwargs
    self.__handle_metadata__["attr"]   = attr
    self.__handle_metadata__["parent"] = parent
  def __getattr__(self, attr):
    return self.__dict__.get(attr,None) or Target(attr=attr, parent=self)
  def __call__(self, *args, **kwargs):
    return Target(*args, attr="__call__", parent=self, **kwargs)
  def __getitem__(self, *args, **kwargs):
    return Target(*args, attr="__getitem__", parent=self, **kwargs)
  def __iter__(self):
    stack = []
    next_handle = self
    while next_handle and (
            next_handle.__handle_metadata__["parent"] or
            next_handle.__handle_metadata__["attr"] ):
      stack.append(next_handle)
      next_handle = next_handle.__handle_metadata__["parent"]
    return iter([ (h.__handle_metadata__["attr"], 
              h.__handle_metadata__["args"],
              h.__handle_metadata__["kwargs"])
            for h in reversed(stack) if h])
