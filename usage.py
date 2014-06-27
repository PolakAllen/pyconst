import const

# a string is an immutable list
@const.Immutable
class String(list):
  def __init__(self, base_str):
    self[:] = list(base_str)

print("""
This application is a brief demo of the immutable functionality.  

@const.immutable
class String(list)
  def __init__(self, base_str):
    self[:] = list(base_str)

The following demonstrations compare a simple String class (which is literally a
list representation of string) to the behavior of a list and the behavior of a
string. 

String is one of the few classes in python which are immutable. Adding more
immutable classes was opened as a PEP (Python Enhancement Proposal), but shot
down due to concerns over performance and violation of the pythonic way.

The immutable decorator created is a so far novel way of creating immutable
objects, and may find a practical niche in debugging.


""")

print("Let's start off with a basic string: 'Hello World'")
hello_String = String("Hello World")
print('\thello_String = String("Hello World")')
hello_list = list("Hello World")
print('\thello_list = list("Hello World")')
hello_str = "Hello World"
print('\thello_str = "Hello World"\n')

print("Here we try setting a 'Hello World' to read 'Mello World'")
print("list has no problems doing the modification")
hello_list[0] = 'M'
assert hello_list == list('Mello World')
print("\thello_list[0] = 'M'")
print("\tassert hello_list == list('Mello World')\n")
try:
  print("We expect a TypeError from str (the native python string)") 
  print("\thello_str[0] = 'M'\n")
  hello_str[0] = "M"
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))
try:
  print("Finally, the behavior of our String class")
  print("\thello_String[0] = 'M'\n")
  hello_String[0] = 'M'
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))

print("Python as has a neat mutability, known as slice modification.")
print('\thello_list[:5] = list("Mello")')
print('\tassert hello_list == list("Mello World")')
hello_list[:5] = list("Mello")
assert hello_list == list("Mello World")
try:
  print('\thello_str[:5] = "Goodbye"')
  hello_str[:5] = "Goodbye"
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))
try:
  print('\thello_String[:5] = "Goodbye"')
  hello_String[:5] = "Goodbye"
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))
  
print("""
What about modification during iteration? 
Note that strings aren't going to cut it, as we can only modify containers""")
list_lists = [[],[],[]]
@const.Immutable
class ListLists(list):
  def __init__(self, lists):
    self[:] = list(lists)
immutable_list_lists = ListLists([[],[],[]])
for i in list_lists:
  i.append('!')
print("\n\t".join("""
list_lists = [[],[],[]]
@const.Immutable
class ListLists(list):
  def __init__(self, lists):
    self[:] = list(lists)
immutable_list_lists = ListLists([[],[],[]])

for i in list_lists:
  i.append('!')
print(list_lists)
""".split('\n')))
print("\t>>>",list_lists)
print("\n\t".join("""
for i in immutable_list_lists:
  i.append('!')
""".split('\n')))
try:
  for i in immutable_list_lists:
    i.append('!')
  print(immutable_list_lists)
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))


print("We even prevent a class from modifying its own internals by default.")
print("\n\t".join("""
@const.Immutable
class NoSelfModification:
  def __init__(self):
    self.static_attr = "Hello World"
    self.container_attr = list("Hello World")
  def mutate_static(self):
    self.static_attr = "Mello World"
  def mutate_container(self):
    self.container_attr.append("!")
no_self_mutate = NoSelfModification()
no_self_mutate.mutate_static()
""".split("\n")))

@const.Immutable
class NoSelfModification:
  def __init__(self):
    self.static_attr = "Hello World"
    self.container_attr = {"Hello":"World"}
  def mutate_static(self):
    self.static_attr = "Mello World"
  def mutate_container(self):
    self.container_attr["World"] = "Hello"

no_self_mutate = NoSelfModification()
try:
  no_self_mutate.mutate_static()
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))

print("\tno_set_mutate.mutate_container()")
try:
  no_self_mutate.mutate_container()
  raise AssertionError("Whoops. Not supposed to be able to modify that")
except TypeError as e: print("\t{}\n".format(e))

