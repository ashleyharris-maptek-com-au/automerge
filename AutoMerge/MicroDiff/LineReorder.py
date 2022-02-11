
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

  oldLinesSet = set(oldLines)
  newLinesSet = set(newLines)

  exactMatches = list(oldLinesSet & newLinesSet)

  freeLinesIn1 = list(oldLinesSet - newLinesSet)
  freeLinesIn2 = list(newLinesSet - oldLinesSet)

  allScores = []

  for fl1 in freeLinesIn1:
    for fl2 in freeLinesIn2:
      allScores.append((Ratio(fl1, fl2), fl1, fl2))

  allScores.sort()

  lineToTextSource = []
  l1sUsed = set()
  l2sUsed = set()

  for score, l1Text, l2Text in allScores:
    if score < 0.6: continue
    if l1Text in l1sUsed: continue
    if l2Text in l2sUsed: continue

    lineToTextSource[l2Text] = l1Text

    l1sUsed.add(l1Text)
    l2sUsed.add(l2Text)

  lineToLineMap = []

  for ln in range(len(newLines)):
    lnText = newLines[ln]

    if lnText in exactMatches:
      loText = lnText
      if oldLines.count(loText) != 1: continue
    elif lnText in lineToTextSource:
      loText = lineToTextSource[lnText]
      if oldLines.count(loText) != 1: continue
    else:
      continue

    sourceIndex = oldLines.index(loText)

    lineToLineMap.append((sourceIndex, ln))

  lineToLineMap.sort()

  reorderedLines = []

  for a, b in Pairwise(lineToLineMap):
    if b[0] > a[0] and b[1] > a[1]: continue

    reorderedLines.append((
      oldLines[a[0]],
      oldLines[b[0]],
      newLines[a[1]],
      newLines[b[1]]))

  raise NotImplementedError()

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
  ""","""
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.ComponentModel;
using System.Windows;
using System.Windows.Data;
using System.Windows.Data.ExtraThingy;
using JetBrains.Annotations;
  """)
