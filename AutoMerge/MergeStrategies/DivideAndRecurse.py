from Merge import Merge
import DiffSolver

def Solve(m : Merge):
  """
  Too hard? Maybe find a common point in all 3, (or 2 of the 3 if one side
  is empty) and see if we can make any progress by solving multiple parts
  of the merge concurrently.

  2 approaches are needed:

  - Find an substantial line in the middle of all 3.
  - Find an empty line which the before and after are roughly similar in all 3.


  """