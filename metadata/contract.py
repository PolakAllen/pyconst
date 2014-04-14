import decorator
import types
import weakref

def Functional(decorator): #future: fields=False, live=False
  """
  A powerful meta-decorator
  takes fn and creates safely wrapped version of original
  also will apply given decorator to a function, or to each member function
  
  future: live means dynamically adding the the class ensures that the new 
  function is wrapped as well
  """
  def wrapper(obj):
    if type(obj) is types.FunctionType:
      return decorator(obj)
    if type(obj) is type:
      for k,v in obj.__dict__.items():
        if type(v) is types.FunctionType:
          obj.__dict__[o] = decorator(obj.__dict__[o])
      return obj 
  return wrapper

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
  
def assert_contracts_dynamic_factory(obj)
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
  return AssertBase(assert_contracts_dynamic_factory)


def Contract(decorator):
  """
  A meta-decorator
  contract decorators add themselves to the object in question,
  to be validated later by @Assert
  """
  def contract(obj):
    if not "__decoratorbase__" in obj:
      setattr(obj, "__decoratorbase__", obj)
    if not "__contracts__" in obj:
      setattr(obj, "__contracts__", [])
      obj = assercontracts(obj)
    if not decorator in obj.__contracts__:
      obj.__contracts__.append(decorator)
    return obj
  return Assert(contract)


