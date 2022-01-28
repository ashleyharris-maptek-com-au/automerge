from Merge import Merge
import DiffSolver
from DiffCalcs.U import fuzzyLineFind

def _FindSplitPoint3(m : Merge):
  a = m.actual
  if len(m.expected) < len(a): a = m.expected
  if len(m.new) < len(a): a = m.new

  bestSplitRatio = 0.8
  bestSplit = None

  for maybe in a.splitlines():
    matchA, matchRatioA = fuzzyLineFind(maybe, m.actual)
    matchE, matchRatioE = fuzzyLineFind(maybe, m.expected)
    matchN, matchRatioN = fuzzyLineFind(maybe, m.new)

    matchRatio = min(matchRatioA, matchRatioE, matchRatioN)

    if matchRatio > bestSplitRatio:
      bestSplitRatio = matchRatio
      bestSplit = (maybe, matchA, matchE, matchN)

  return bestSplit

def _FindSplitPoint2(str1 : str, str2 : str):
  bestSplitRatio = 0.8
  bestSplit = None

  for maybe in a.splitlines():
    match, matchRatio = fuzzyLineFind(maybe, a)

    if matchRatio > bestSplitRatio:
      bestSplitRatio = matchRatio
      bestSplit = (maybe, match)

  return bestSplit

def Solve(m : Merge):
  """
  Too hard? Maybe find a common point in all 3, (or 2 of the 3 if one side
  is empty) and see if we can make any progress by solving multiple parts
  of the merge concurrently.

  2 approaches are needed:

  - Find an substantial line in the middle of all 3.
  - Find an empty line which the before and after are roughly similar in all 3.

  """

  