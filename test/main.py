#!/usr/bin/python3

from const import immutable, modifies, Params
import unittest

"""
We'll combine a set of decorator conditions on a set of class methods.
As the decorator conditions are the same for each class method, we'll make a
helper function to unpack them for us
"""

class ArrayContainer:
  def __init__(self):
    self.assign()

  def get(self):
    return self.t
  def assign(self):
    self.t = [1]
  def modify(self):
    self.t.append(1)
  def delete(self):
    del self.t

  """
  def get_sub(self):
    return self.t[0]
  def assign_sub(self):
    self.t[0] = []
  def modify_sub(self):
    self.t[0].append([])
  def delete_sub(self):
    del self.t[0]
    """

decorators = {
  "no_decorator": lambda _: _,
  "general": modifies(Params().self),
  "specific": modifies(Params().self.t),
  "invalid_parameter": modifies(Params().badparam),
  "wrong_attribute": modifies(Params().self.x)
}
for name in { "assign", "modify", "delete", 
              "assign_sub", "modify_sub", "delete_sub" }:
  for description, decorator in decorators.items():
    setattr(ArrayContainer,"_".join([name,description]),decorator)
  
ArrayContainer = immutable(ArrayContainer)

class main(unittest.TestCase):
  def test_correct_specifications_behave_correctly(self):
    instance = ArrayContainer()
    self.assertCountEqual(instance.t,[1])
    instance.assign_general()
    self.assertCountEqual(instance.t,[1])
    instance.assign_specific()
    self.assertCountEqual(instance.t,[1])
    #instance.assign_sub_general()
    #assert instance.t == [[[]]]
    #instance.assign_sub_specific()
    #assert instance.t == [[[]]]
    instance.mutate_general()
    self.assertCountEqual(instance.t,[1,1])
    instance.mutate_specific()
    self.assertCountEqual(instance.t,[1,1,1])
    #instance.mutate_sub_general()
    #assert instance.t == [[[]]]
    #instance.mutate_sub_specific()
    #assert instance.t == [[[[]]]]

if __name__ == "__main__":
  unittest.main()
