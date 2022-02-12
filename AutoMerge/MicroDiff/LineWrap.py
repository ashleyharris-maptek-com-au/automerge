"""
Represents line(s) being surrounding by new lines.

"""

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

import difflib
import LandmarkLib


class LineWrap:
  def __init__(self) -> None:
    self.lineWrappings = {}

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  lineToLineMap, halfWayLines = LineToLineMapAndHalwayMap(oldLines, newLines)

  equalRanges = difflib.SequenceMatcher(None, oldLines, halfWayLines).get_matching_blocks()

  presents = []

  for a, b, c in Triplewise(equalRanges):
    oldLeft = oldLines[a.a + a.size : b.a]  
    oldRight = oldLines[b.a + b.size : c.a]  

    if len(oldLeft) or len("".join(oldLeft).strip()): continue
    if len(oldRight) or len("".join(oldRight).strip()): continue

    newLeft = halfWayLines[a.b + a.size : b.b]  
    newRight = halfWayLines[b.b + b.size : c.b]  

    if len(newLeft) == 0 or len(newRight) == 0: continue

    selectorBegin = LandmarkLib.DescribeLine(oldLines, b.a)
    selectorEnd = None

    if b.size > 1:
      selectorEnd = LandmarkLib.DescribeLine(oldLines, b.a + b.size - 1)

    presents.append((
      oldLines[b.a : b.a + b.size],
      newLines[b.b : b.b + b.size],
      selectorBegin,
      selectorEnd,
      newLeft,
      newRight))


  if len(presents): return None
  lw = LineWrap()
  lw.lineWrappings = presents
  return lw

if __name__ == '__main__':
  Process("""
#include <abcfdefe>
#include <Windows.h>
#include <dfsgdfg/asdasdsad>
  """.strip(),"""
#include <include/abcfdefe>

#if COMPILE_FOR_WINDOWS
#include <Windows.H>
#else
#include <sys/resource.h>
#endif

#include <include/dfsgdfg/asdasdsad>
  """.strip())
