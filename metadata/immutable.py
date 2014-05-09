
from metadata.contract import DynamicContract
from metadata.injector import sentinal
from decorator import decorator
import types

class MutationError(Exception):
  def __str__(self):
    return self.msg

class FieldMutation(MutationError):
  def __init__(self, mutated, point, value):
    self.msg = "@Immutable: {}.{} != {}".format(mutated, point, value)

class ObjectMutation(MutationError):
  def __init__(self, mutated, point):
    self.msg = "@Immutable: {} not in {}".format(point, mutated)

class ObjectMutation(MutationError):
  def __init__(self, mutated, point):
    self.msg = "@Immutable: cannot delete {} from {}".format(point, mutated)

def mutation_set(self, obj, value):
  if hasattr(self, obj):
    if self.obj != value:
      raise FieldMutation(self, obj, value)
  else:
    raise ObjectMutation(self, obj)

def Immutable(obj):
  """
  print(obj.__init__.__name__)
  original_init = obj.__init__
  def freeze(self, *args, **kwargs):
    print("trying frozen __init__")
    original_init(self, *args, **kwargs)
    if hasattr(obj, "__dict__"):
      for k,v in obj.__dict__.items():
        val = sentinal(v, mutation_set)
        if not v is val:
          setattr(obj, k, val)
  obj.__init__ = freeze
  print(obj.__init__.__name__)
  """
  return sentinal(obj, mutation_set)

@Immutable
class Test:
  pass
