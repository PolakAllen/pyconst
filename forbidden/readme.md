Forbidden
=========

Introduction
------------

Assertions and metaproperties provide a mental framework from which we can 
examine all developments in modern programming langauges and practices.

This project is an experiment which seeks to build on our abstractions of modern
practices, perhaps improving or extending existing paradigms, or perhaps 
discovering new paradigms altogether.

This project is both academic and practical, seeking to bring the best academic
concepts to test in practical situations.

For those interested in the practical side, read "What does it actually do?" and
"Why?" below.

For those interested in the academic side, read "Future Ideas"

What does it actually do?
-------------------------

Right now, it's just a framework for modification validation

We allow the user to assert their sanity when debugging

    @nomutate(globals,file)
    def function_that_might_be_mutating_a_global(...)

Unsure if a class or method might be misbehaving? Monkey patch it

    bad_class = nomutate(globals)(bad_class)
    bad_class.bad_method = nomutate(self)(bad_class.bad_method)

Why document it when you can contract it?

    @maymutate(self.var) # and implicitly, nomutate everything else
    def object_method(can_use_any_variable_name_as_self, ...)

currently only mutations blocking works
mutation assertions can be bound to any object, list, dictionary
mutation assertions can be bound to functions as well

Why?
----

Because we expect that these assertions could be violated. Accidently forgetting
some part of the design, a typographical mistake, or perhaps some
miscommunication.

In short, these are alternative validations, more akin to contract validations,
or static typing.

The experimental nature of this project makes no claims about whether such
things will actually provide any real benefit, though we'd like to test whether
or not it does.

Future Ideas
------------

1. External Graphs

Code reuse is a common concept in all languages, and an essential part of
structured programming. The structure of larger programs is often dependent 
upon strict enforment of the dependency graph, which is typically only 
handled at the highest granularity of code divisions 
(module, class, seperate files, etc.)

The external graph is such a concept at any level of resolution. It is the
external dependecies, outside the given scope, which could be a block, a
closure, a function, a class, etc. We use the word graph, as each item in the
external graph from the given scope will also have an external graph, which
rapidly expands to the complete body of executable code associated to that
orginal scope.

The external graph, or reachable code, is a source of many assertions we may
want to make about a given block of code. For instance, we assume that most of
our code is not multithreaded, not writing large amounts of data to file, etc. 
These assumptions are usually fairly safe, as such functionality is usually
explicitly documented, or relatively obvious from the name.

External graphs may get more use as a higher granularity dependency graph.

2. Internal Graphs

Internal graphs are a far more expermental analogous application of external
graphs. Internal graphs are concerned with any scope that allows definition and
execution of other executable scopes.

Cyclic internal graphs will identify recursion, though it should be noted that
cyclic graphs might be constantly bounded, and not recursive in the traditional
sense.

A non-trivial internal graph is likely a good measure of complexity of a given
unit. We might make assertions about internal graph complexities.

Alternatively, we might make assertions about the internal graph, for the same
reasons we would do so with external graphs. However, this implies a certain
level of complexity of a given scope, which is likely to be discouraged by best
practices. 

An external graph may disreguard the specifics of an internal graph (treating
the entire internal graph as a single root node), though to be an adequate 
external graph, must walk the internal graph as well. We can call a complete
graph, that is to say, an iterative external graph from each of the lowest level
scopes in a given scope, a code graph.

3. Assertion Types

Assertion types are best described by the source of the assertion, the source of
the violation, and type of information being asserted (metatype)

Here is a list of common assertions:

  1. Types (metatype: type, target: data, violation: assignment)
  2. Invariant (metatype: constraint, target: data, violation: assignment)
  3. Precondition (metatype: constraint, target: data, violation: stack)
  4. Postcondition (metatype: constraint, target: data, violation: stack)
  5. Property (metatype: property, target: block, violation: target)

Its likely that most readers treat Types as a conceptually distinct concept
from assertions. Types are an interpretation of structured data, and most typing
systems make assertions about type relations. These assertions allow us to make
interesting relations 

4. Progressive Analysis

Static analysis tools use source code to predict program behavior, and there are
numerous runtime tools that analyze the running behaviors. 

However, one wonders if there are any tools which predict program behaviors from
source, using runtime information.

Such tools probably don't exist as they're prohibitively expensive to run. We can
likely provide pre-compiled structures to analyze some specific behavior, but
doing so will be very much dependent upon the specific behavior being validated.

A method of providing such a functionality is experimented with in this project.
We assume that all effects of a program or subprogram are within its side
effects and functional return values. We also assume that the fastest, most
efficent, and most reliable way to predict program behavior is to simply run the
program and look at the result.

If we assume the above, we find sub-program sandboxing to be an efficent manner
to proceed. That is to say, when we wish to validate functionality, we run the
program in a special mode which virtualizes all operations. Global side effects
(effects outside our program) are not executed until after validation of the
program. Validations make sense on a per-stack basis, though further experiments
could be done on a multistack (multi-thread/process) basis. As such mutations
are proxied as well.

The practically of the above is likely to be very limited, as global side
effects are often carefully controlled, and occur relatively infrequently, apart
from logging, which we often want to occur in an validation violation context
anyways.

Alternatively, we could use the same progressive analysis to provide more
detailed logs, on a violation. This is likely are much more useful usecase.

5. Assertion Insertions (AOP assertions)

We might assume that the assertions we want to use are best located just outside
the scope of interest, but its likely that we'd want to make assertions about
existing code without source modification.

In order to be usable, we'd want a precise grammar for selecting blocks.
Our joinpoints of interest would be any valid location for an assertion. Our
assertions come in two primary forms, stack based (modal), and
invariant (static).

In addition, assertions allow us to reason about program behavior. A sufficently
advanced assertion framework may generate a new paradigm that affords a seperate
specification of behaviors.
