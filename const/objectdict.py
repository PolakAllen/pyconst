class ObjectDict:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
  def __setitem__(self, item, value):
    self.__dict__[item] = value
  def __getitem__(self, item):
    return self.__dict__[item]
  def __delitem__(self, item):
    del self.__dict__[item]

class Struct:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
  def __getitem__(self, item):
    return self.__dict__[item]
