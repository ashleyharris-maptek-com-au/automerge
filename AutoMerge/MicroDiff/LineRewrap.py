"""
=# 

Represents the rewrapping of a line - ie moving around tabs, spaces, and newlines.

Note we don't have the ability to "re-apply" it - you should be using a tool like
clang-format after a merge resolution, and the ability to decode format, and re-appply it,
is beyond the scope of this tool.

=Old
functionCall(abc,
             def,
             ghi);
=New
functionCall(
  abc, def, ghi);
=Expect
"""

import re
import itertools
import difflib
import LandmarkLib
import os
from dataclasses import dataclass


try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

@dataclass
class WrapArea:
  firstLine : LandmarkLib.LineSelector
  lastLine : LandmarkLib.LineSelector
  lineBreakSelectors : list[LandmarkLib.CharacterRangeSelector]


class LineRewrap:
  def __init__(self) -> None:
    
    self.wrapAreas = []

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  lineToLineMap = LineToLineMap(oldLines, newLines)

  