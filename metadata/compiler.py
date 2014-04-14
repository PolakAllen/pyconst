#!/usr/bin/python3
import inspect
import ast
import types
import testmodule
"""
Generates metadata and attaches it to python objects

We walk through the source, and provide living definitions to scoped variables.
This allows us to predict behaviors at various points in function execution

Impossible you say? No, just hard. NP-Hard. But hey, caching results is NP-cool,
and given that most the only NP hard part is the stuff that hasn't been done
before.

Anyway, what's the point?

We can uses @annotations to intercept function calls and provide a more detailed
(deterministic) analysis at various points.

Or, more specifically, we provide static analaysis of 

These annotations provide some basic rules for the Local and State objects
associated with a given context.

What kind of metadata?
  - Context 
    usage: "obj.__context__['name']"
    Associated with modules, function defintions, classes, lambdas,
    contextmanagers, if/for/while, or anything else that defines a context

    returns a <State> wrapper if 'name' is nonlocal, otherwise <Local>

  - ContextGraph
    usage: "for context in obj.__contextgraph__"
    Some of the things that are Contexts are inaccessible by conventional means
    (good luck hooking into that 'if' statement)

  - Local 
    usage:  "s = obj.__context__['localvar']"
            "s.at(line or obj.__contextgraph__[1])"
            "s.from(line or obj.__contextgraph__[1]).at(line)"
    We usually want to know whats happened to a given object in a procedure
    

  - State as Local (but on a
    Note: must have a procedural context. Ignores what may happen outside of

    procedure
  - CallGraph
How to use?

"""

class Context(dict):
  "Provides proper resolution for variables"
  def __init__(self, node, parent=None):
    "parent assumed to be dictionary or Context. Will be searched recursively"
    self.parent = parent
    self.node = node
    self.scopes = [parent] if parent else []
    if type(node) is types.ModuleType:
      scopes_lookup = ["__dict__","__builtins__"]
    if type(node) is types.FunctionType:
      # this should be the parent, but allow override
      self.parent = self.parent or node.__globals__
      self.scopes = [self.parent]
      # chain into __code__ object (we need to look at locals there)
      node = node.__code__
    if type(node) is types.CodeObject
      # dictify local variables
      
    if scopes_lookup:
      self.scopes += [getattr(node,d) for d in scopes_lookup if d in node]

  def namesinscope(self, item):
    scopes = []
    for s in self.scopes:
      if item in s:
        scopes.append(s[item])
    return scopes

  def findit(self, item):
    # regular functions have a __globals__ object
    if type(self.context) is types.FunctionType:
      self.context = self.context.__code__
    # but locally defined functions do not
    if type(self.context) is types.CodeType:
      tryorder = ["__globals__"]
      # we need to try and find it locally first
      checkin = ["co_
    for d in tryorder: 
      keys = d.split(".")
      print("trying to find",item,"in",self.context,".",d)
      next_ = self.context
      for k in keys:
        next_ = getattr(next_,k,[])
        if k not in next_: break

      if item in next_:
        return d, next_[item]

class ExternalGraphWalker(ast.NodeVisitor,dict):
  """
  Have you ever wanted to see what your function calls?
  No?

  Well, in case you did, you can use the amazing, fantasical, stupendously stupid
  ExternalGraphWalker class to see them...

  Needs a scope context currently. Will lookup things in scope and give you the
  actual context and existing code object. 
  """
  def __init__(self, context):
    self.context = context
  def __missing__(self, context):
    self[context] = rv = []
    return rv


  def generic_visit(self, node):
    #print(type(node).__name__)
    if type(node) == ast.FunctionDef:
      _,self.context = self.findit(node.name)
      if not self.context:

    if type(node) == ast.Call:
      self[self.context].append(node.func.id)
      print("Calling",node.func.id)
      _,self.context = self.findit(node.func.id)
    ast.NodeVisitor.generic_visit(self, node)

def compile():
  with open("testmodule.py", "r") as f:
    node = ast.parse(f.read())
  graphwalk = ExternalGraphWalker(testmodule)
  graphwalk.visit(node)
  print(graphwalk)


if __name__ == "__main__":
  compile()
