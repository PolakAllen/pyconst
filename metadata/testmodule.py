import re
from metadata.immutable import Immutable
from metadata.contractassert import DynamicAssert

@Immutable
class CreatesNonModifyableInstances:
  def __init__(self, a):
    self.a = a

def validuse():
  "We should see 'Hello World'"
  instance = CreatesNonModifyableInstances("Hello")
  print(instance)
  print(instance.a + "World")

def partialexecuteinvalid():
  "We should see 'Before modification' but no 'Hello World'"
  instance = CreatesNonModifyableInstances("Hello")
  print("Before modification")
  instance.a = "Hello World"
  print(instance.a)

#@DynamicAssert
def noexecuteinvalid():
  "We should see no 'Before modification' message"
  instance = CreatesNonModifyableInstances("Hello")
  print("Before modification")
  instance.a = "Hello World"
  print(instance.a)

if __name__ == "__main__":
  validuse()
  try:
    partialexecuteinvalid()
  except Exception as e:
    print("We expected to see an exception:")
    print("\t",e)
  try:
    noexecuteinvalid()
  except Exception as e:
    print("We expected to see an exception:")
    print("\t",e)
  validuse()
