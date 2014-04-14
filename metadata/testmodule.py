import re

def modulegfunc():
  def localfn(toprint):
    print(toprint)
  localfn("Hello World!")

def helloworld():
  modulegfunc()
