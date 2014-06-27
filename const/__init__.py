from const.mode import *
from const.proxy import Immutable, nomutate
from const.target import Target as Params
from functools import wraps
import types

"""
@Immutable class
  A class's object attributes are unable to be set, and the property is recursive
  meaning an attribute returned from the class is also @Immutable. Note that
  recursive attributes are not complete immutable, as the defining class is not
  considered immutable by other code.

@nomutate(Target...) fn
  inject an @Immutable proxy into the annotated function, based on the desired
  target.

# TODO
@mutates(Target...) fn
  override a prior immutable proxy

We still need __metastack__ for making assertions about mutations in variables
outside of the parameters and class members of a given block. No features
currently rely on __metastack__, but its being left as part of the framework for
specifying metadata
"""

