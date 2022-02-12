
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

import LandmarkLib

class LineReorder:
  def __init__(self) -> None:
    self.lineToLineMap = {}

  def apply(self, string : str):
    pass # return string, cost
    
  #def __repr__: pass


def Process(old : str, new : str):
  oldLines = old.splitlines()
  newLines = new.splitlines()

  lineToLineMap = LineToLineMap(oldLines, newLines)

  lineToLineMap.append((-1, -1))
  lineToLineMap.sort()

  reorderedLines = 0

  for a, b in Pairwise(lineToLineMap):
    if b[0] > a[0] and b[1] > a[1]: continue

    reorderedLines += 1

  if reorderedLines == 0: return None

  lineMap = []

  unhandledLines = set(range(len(newLines)))

  for a, b in Pairwise(lineToLineMap):
    lineDeltaOld = b[0] - a[0]
    lineDeltaNew = b[1] - a[1]

    if oldLines[b[0]].strip() == "" and newLines[b[1]].strip() == "": 
      lineMap.append((None, b[0], b[1], "", ""))
      unhandledLines.remove(b[1])
      continue

    if lineDeltaNew == 1 and lineDeltaOld == 1 or b[0] == b[1]: 
      lineMap.append((None, b[0], b[1], oldLines[b[0]], newLines[b[1]]))
      unhandledLines.remove(b[1])
      continue

    lineMap.append((
      LandmarkLib.DescribeLine(oldLines, b[0]), 
      b[0], b[1], 
      oldLines[b[0]], newLines[b[1]]))

    unhandledLines.remove(b[1])

  for uh in unhandledLines:
    if newLines[uh].strip() == "": continue

    lineMap.append((None, None, uh, None, newLines[uh]))


  lr = LineReorder()

  lr.lineToLineMap = lineMap

  return lr


if __name__ == '__main__':
  Process("""
using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Linq;
using System.Windows;
using System.Windows.Data;

using JetBrains.Annotations;

using System.ComponentModel;
  """.strip(),"""
using ExtraImports;

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.ComponentModel;
using System.Windows;
using System.Windows.Data;
using System.Windows.Data.ExtraThingy;

using JetBrains.Annotations;
  """.strip())
