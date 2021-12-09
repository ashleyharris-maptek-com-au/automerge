from Merge import Merge
import DiffSolver

def Solve(m : Merge):
  """
  The most common merge conflict - 2 people make different edits to the
  same common revision.

          /- Change A -\ 
   Start -              ARGH!      Start->Change A->Change B->Phew!
          \- Change B -/

  """

  class Option:
    def __init__(self) -> None:
      self.changeSequence = None
      self.appliedTo = ""
      self.cost = 0
    pass

  allOptions = []

  expToActOptions = DiffSolver.AllPossibleSolutions(m.expected, m.actual)

  for path in expToActOptions:
    o = Option()
    o.changeSequence = path
    o.appliedTo = "ea"
    o.cost = path.cost
    allOptions.append(o)

  expToNewOptions = DiffSolver.AllPossibleSolutions(m.expected, m.new)

  for path in expToNewOptions:
    o = Option()
    o.changeSequence = path
    o.appliedTo = "en"
    o.cost = path.cost
    allOptions.append(o)

  allOptions.sort(key = lambda x : x.cost)

  allResults = {}

  for opt in allOptions:
    active = ""

    if opt.appliedTo == "en":
      active = m.actual
    else:
      active = m.new

    activeRes = opt.changeSequence.applyTo(active)

    if activeRes in allResults: allResults[activeRes] += 1
    else: allResults[activeRes] = 1

  return allResults