#!/usr/bin/python3

from const.proxy import ProxyDispatch
import unittest

class TestProxy(unittest.TestCase):
  def setUp(self):
    self.proxysource = ProxyDispatch()

  def test_unmodified_primatives(self):
    # float
    Float = self.proxysource.get_class(float)
    f1 = Float(1.0)
    f2 = Float(2.0)
    assert str(f1) == "1"
    assert isinstance(f1, float)
    assert f1 == 1.0
    assert -f1 == -1.0
    assert f1 != 1.000001
    assert f1 + f2 == 3.0
    assert f2 + f1 == 3.0
    assert f1 - f2 == -1.0
    assert f2 - f1 == 1.0
    assert f2 / f1 == 2.0
    assert f1 / f2 == 0.5
    assert f1 * f2 == 2.0
    assert f2 * f1 == 2.0

    # int
    Int = self.proxysource.get_class(int)
    i1 = Int(1)
    i2 = Int(2)
    assert str(i1) == "1"
    assert isinstance(i1, int)
    assert f1 == 1
    assert -f1 == -1
    assert f1 != 2
    assert i1 + i2 == 3
    assert i2 + i1 == 3
    assert i1 - i2 == -1
    assert i2 - i1 == 1
    assert i2 / i1 == 2
    assert i1 / i2 == 0
    assert i1 * i2 == 2
    assert i2 * i1 == 2

    # string
    String = self.proxysource.get_class(str)
    s1 = Str("1")
    s2 = Str("2")

if __name__ == "__main__":
  unittest.main()
