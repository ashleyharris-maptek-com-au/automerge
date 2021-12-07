from Merge import Merge
import DiffSolver
import MergeSimplifiers
import itertools

def SolveMerge(m : Merge):
  
  # Can decode Change A or B such that this transform works?

  #        _- Change A
  # Start -                    Start->Change A->Change B
  #        -- Change B

  merge = m
  while True:
    anyChange = False
    for ms in MergeSimplifiers.allMergeSimplifiers:
      m2 = ms(merge)
      if m2:
        merge = m2
        anyChange = True
    if anyChange == False: break

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

  solvedSequences.sort(key = lambda x : x.cost)

m = Merge()
m.fromString("""
<<<<<<<
    Tstring i = "";
|||||||
    std::vector<sysC_Path> destinations = {expectedImage};
    Tstring i = "";
=======
    std::vector<sysC_Path> destinations = {expectedImage};
    Tstring i = "a";
>>>>>>>
""")

SolveMerge(m)