
def range(i):
  class obj:
    def __iter__(self):
      j = 0
      while j < i:
        yield j
        j += 1
  return obj()

class Test(list):
  def __init__(self, *args, **kwargs):
    self.__dict__.update(**kwargs)
    self[:] = args
