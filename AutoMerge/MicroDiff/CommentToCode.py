
"""
Represents a chunk of code that was commented out being renabled.
"""



import re
import itertools
import difflib
import LandmarkLib
import os

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

class Uncommented:
  def __init__(self) -> None:
    self.codeRegionsToUncomment = []

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  lineToLineMap, halfWayLines = LineToLineMapAndHalwayMap(oldLines, newLines)

  # We need to consider cases like
  # // blah-> blah(
  # //   blah)
  #
  #    ->
  #
  # blah->blah(blah)
  #
  # As it's quite common for commenting chunks of code to increase the column witdth,
  # requiring a re-wrap of the code. Code could also be uncommmented and changed - 
  # especially if code was commented out for having a bug, and then uncommented with
  # a fix in the same commit.


  for oL, nL, index in zip(halfWayLines, newLines, index):



