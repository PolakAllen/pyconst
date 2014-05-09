from decorator import decorator
import functools as ft

def AssertBase(assertcontracts):
  def Assert(obj):
    if not hasattr(obj,"__contracts__"):
      # do some static analysis to generate __contracts__
      # as contracts may be in function body
      pass
    use = obj
    if not hasattr(obj,"__assertscontracts__"):
      use = assertcontracts(obj)
      setattr(obj, "__assertscontracts__", assertcontracts)
    return use
  return Assert
  
def assert_contracts_dynamic_factory(obj):
  @decorator(obj)
  @ft.wraps(obj)
  def assert_contracts_dynamic(states, args, kwargs):
    for contract in obj.__contracts__:
      contract.validate(states, args, kwargs, obj)
  return assert_contracts_dynamic

def DynamicAssert(obj):
  """
  @DynamicAssert
  runs the wrapped block in simulation mode.
  contracts are validated against inputs, outputs and changelist
  """
  return AssertBase(assert_contracts_dynamic_factory)(obj)
