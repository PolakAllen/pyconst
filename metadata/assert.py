import decorator

def Assert(fn):
  """
  @Assert

  checks that the wrapped block violates no contracts with the given inputs
  """
  if not hasattr(fn,"__contracts__"):
    # do some static analysis to generate __contracts__
  @decorator(fn)
  def assertcontracts(*args, **kwargs):
    for contract in fn.__contracts__:
      contract.validate(*args, **kwargs)
    fn(*args, **kwargs)

  return assertcontracts


