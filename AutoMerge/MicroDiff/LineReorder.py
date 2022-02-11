
import re
import itertools
import difflib

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

neightbourRegex = r"([^\w\s]*)"

class ReplaceToken:
  def __init__(self) -> None:
    self.tr = {}

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass


def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  oldLines.sort()
  newLines.sort()

