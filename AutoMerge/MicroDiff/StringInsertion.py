

"""
Represents a dumb chunk of text being inserted. This is fairly high cost operation, as it's very
fallible when applied to different code and should be a last resort - token and line change diffs.

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


import MicroDiff.StringDeletion

class StringInsertion:
  def __init__(self) -> None:
    self.chunksToInsert = []

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oldLines = old.splitlines()

  # An insertion is the mirror of a deletion, so use that code:
  dc = MicroDiff.StringDeletion.Process(new, old)

  lineSelectors = {}

  si = StringInsertion()

  for reverseLineSelector, lineNo, reversedCharSelector, string in dc.chunksToDelete:

    lineSelector = None

    if lineNo not in lineSelectors:
      lineSelector = LandmarkLib.DescribeLine(oldLines, lineNo)
      lineSelectors[lineNo] = lineSelector
    else:
      lineSelector = lineSelectors[lineNo]

    if oldLines[lineNo].count(string) != 1:
      raise NotImplementedError()

    index = oldLines[lineNo].find(string)

    charSelector = LandmarkLib.DescribeCharacterRange(
      oldLines[lineNo],
      index,
      index + len(string))

    si.chunksToInsert.append((lineSelector, charSelector))

  return si


if __name__ == '__main__':
  Process(
    "First ultra basic test of string deletion diff thingy.", 
    "First ultra basic test of string<a list of chars> deletion diff thingy.")

