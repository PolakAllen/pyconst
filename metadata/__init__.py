
"""
The execution of a python program at any given point can be known, but often
only after execution.

The purpose of this project is to provide a static analasis framework which 
progressively adds more data during execution, as it becomes available.

Such a framework works by analysing ASTs and providing proxied references to the
partial results therein. This allows us to both predict how the program will
behave, and, based on the results so far, predict the next result.

For example, basic static analysis can tell us everything we need to know about
this snippet:

  def foo():
    a = [1,2,3]
    b = 1
    return a[b]

but it can't reliably predict the result of:

  def foo(a):
    b = 1
    return a[b]

The point of this project is to allow progressive inferences.

For instance, if we wish to assert that a function doesn't modify its internals,
we might make the following assertion:

  class Bar:
    def foo(self):
      self.a = 1
      assert false  # we modified an internal

Which could be easily caught by a static analysis program.
However,

  class Bar:
    def foo(self, fn):
      return fn(self)
      # no idea if we modified it or not

is far less predictable.
The @Immutable annotation provides a way to catch such violations at run time,
before function execution

  def goodfn(s): 
    return "Hello World!"

  def badfn(s): 
    s.a = 1

  @Immutable
  class Bar:
    def foo(fn):
      return fn(self)

  # is okay
  Bar().foo(goodfn)

  # throws ContractError("@Immutable Bar violation in {context}")
  Bar().foo(badfn)

Such violations can be caught further up as well

  # throws ContractError("@Immutable Bar violation in main() line 8")
  @Assert
  def main():
    Bar().foo(goodfn)
    Bar().foo(badfn)

or even

  @Assert
  def main(fn):
    somethingelse()
    Bar().foo(fn)

  # throws ContractError("@Immutable Bar violation in main() line 8")
  main(badfn)

Similarly, objects returned can be infected:

  @Immutable
  class Bar:
    a = []

  # throws ContractError("@Immutable Bar violation in {context}")
  Bar().a.append(1)

Other important assertions:
  @Deterministic - Do we have sufficent information to form good contracts
  @Terminates    - Assert that the problem terminates

Problems:
  the double dispatch
"""
  
  
