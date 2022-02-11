
import re
import itertools

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
  oldTokens = TokenAndGrammar(old)
  #newTokens = TokenAndGrammar(new)

  maybeMatches = []

  for a,b,c in Triplewise(oldTokens):
    reg = re.compile(
      re.escape(a) + r"\s*" +
      re.escape(b) + r"\s*" +
      re.escape(c))

    allMatchesInOld = list(re.finditer(reg, old))
    allMatchesInNew = list(re.finditer(reg, new))

    if len(allMatchesInOld) == 0 or len(allMatchesInNew) == 0:
      continue

    if len(allMatchesInOld) == len(allMatchesInNew):
      for d,e in itertools.zip_longest(allMatchesInOld, allMatchesInNew):
        d0, d1 = d.span()
        e0, e1 = e.span()
        
        for r in [0, 0.25, 0.5, 0.75, 1.0]:
          dr = (d1 - d0) * r + d0
          er = (e1 - e0) * r + e0

          maybeMatches.append((int(dr),int(er), old[d0:d1], new[e0:e1]))

    elif len(allMatchesInNew) == 1:
      e0, e1 = allMatchesInNew[0].span()
      for d in allMatchesInOld:
        d0, d1 = d.span()
        dr = (d1 - d0) * r + d0
        
        for r in [0, 0.25, 0.5, 0.75, 1.0]:
          er = (e1 - e0) * r + e0

          maybeMatches.append((int(dr),int(er), old[d0:d1], new[e0:e1]))


    elif len(allMatchesInOld) == 1:
      d0, d1 = allMatchesInOld[0].span()

      for e in allMatchesInNew:
        e0, e1 = e.span()
        er = (e1 - e0) * r + e0
        
        for r in [0, 0.25, 0.5, 0.75, 1.0]:
          dr = (d1 - d0) * r + d0

          maybeMatches.append((int(dr),int(er), old[d0:d1], new[e0:e1]))

  matches = sorted(maybeMatches)

  lineToLineMap = Dict0()

  for match in matches:
    oldLine = old[0:(match[0])].count("\n")
    newLine = new[0:(match[1])].count("\n")

    lineToLineMap[(oldLine, newLine)] += 1

  raise NotImplemented()

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