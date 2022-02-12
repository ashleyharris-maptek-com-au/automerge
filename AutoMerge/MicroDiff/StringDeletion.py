
"""
Represents a dumb chunk of text being removed. This is fairly high cost operation, as it's very
fallible when applied to different code and should be a last resort - token and line removal
diffs are much more portable.

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

class StringDeletion:
  def __init__(self) -> None:
    self.chunksToDelete = []

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass

def Process(old : str, new : str):

  sd = StringDeletion()

  if old.strip().count("\n") or new.strip().count("\n"):
    oldLines = old.splitlines()
    newLines = new.splitlines()

    lineToLineMap = LineToLineMap(oldLines, newLines)

    for ol, nl in lineToLineMap:
      ot = oldLines[ol]
      nt = newLines[nl]

      if ot == nt: continue
      if ot.strip() == nt.strip(): continue

      sdd = Process(ot, nt)

      if sdd is None: continue

      lineDescriptor = LandmarkLib.DescribeLine(oldLines, ol)

      for q, charSelector, text in sdd.chunksToDelete:
        sd.chunksToDelete.append((
          lineDescriptor, ol, charSelector, text))

    return sd
  else:
    old = old.strip()
    new = new.strip()

    cp = os.path.commonprefix([old, new])
    cs = os.path.commonprefix([old[::-1], new[::-1]])[::-1]

    if new == cp + cs: 
      sd.chunksToDelete.append((
        None,
        None,
        LandmarkLib.DescribeCharacterRange(old, len(cp), len(old) - len(cs)),
        old[len(cp) : len(old) - len(cs)]))
      return sd
    else:
      middleBit = old[len(cp) : len(old) - len(cs)]

      if middleBit not in old:
        # This isn't 2 removes around a common middle ground
        return None

      mbo = old.index(middleBit)

      sd.chunksToDelete.append((
        None,
        None,
        LandmarkLib.DescribeCharacterRange(old, len(cp), mbo),
        old[len(cp) : mbo]))

      sd.chunksToDelete.append((
        None,
        None,
        LandmarkLib.DescribeCharacterRange(old, mbo, len(old) - len(cs)),
        old[mbo : len(old) - len(cs)]))

      return sd


if __name__ == '__main__':
  Process(
    "First ultraReallyBasic test of string deletion diff thingy.", 
    "First ultraBasic test of string deletion diff thingy.")

