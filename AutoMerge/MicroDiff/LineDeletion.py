"""
=# 

Represents the deletion of a line.

=Old
#ifdef WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif
=New
#ifdef WINDOWS
#include <Windows.H>
#endif
=Expect
Remove Line "#include <opengl.H>"
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

class LineDeletion:
  def __init__(self) -> None:
    self.linesToDelete = []

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  lineToLineMap = LineToLineMap(oldLines, newLines)

  lines = set(range(len(oldLines)))

  for f, t in lineToLineMap:
    lines.remove(f)

  for li, lv in zip(range(len(oldLines)), oldLines):
    if lv.strip() == "": lines.remove(li)

  initialScore = RatioToken(old, new)

  ld = LineDeletion()

  for l in lines:
    oldRemoved = oldLines[:]
    del oldRemoved[l]

    oldRemovedText = "\n".join(oldRemoved)

    newScore = RatioToken(oldRemovedText, new)

    if newScore > initialScore:
      # The diff becomes better by removing this line.
      ld.linesToDelete.append(
        LandmarkLib.DescribeLine(oldLines, l))

  if len(ld.linesToDelete) == 0: return None

  return ld

if __name__ == '__main__':
  Process("""
#ifdef WINDOWS
#include <Windows.H>
#include <opengl.H>
#endif
    """.strip(), """
#if defined(WINDOWS)
#include <Windows.H>
#endif
    """.strip())

