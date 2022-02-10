"""
MicroDiffs are small, localised changes to a chunk of text.

These include things like:
- A token has changed.
- 2 tokens have swapped position
- Indentation has increased
- A string has been found/replaced
- A string was inserted between 2 tokens
- 2 lines have swapped

etc.

Microdiffs analysis uses O(N^lots) algorithms, and should never be run over more
than about 5 lines of text, or run over text that is radically different. Use 
MegaDiffs to narrow down the scope and find similar regions.


"""

import pkgutil
import pathlib
import sys, os
folderPath = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(folderPath)

allDiffGenerators = []

for a in pkgutil.iter_modules([os.path.join(folderPath,'MicroDiff')]):
  exec("from MicroDiff import " + a.name + " as t")

  if "Process" in dir(t):
    allDiffGenerators.append(t.Process)



class ChangeSequence:
  def __init__(self, start, target) -> None:

    self.start = start
    self.actual = start
    self.target = target

    self.score = difflib.SequenceMatcher(None,start,target).ratio()
    self.cost = 0

    self.steps = []
   
  def append(self, diff):
    self.steps.append(diff)
    result = diff.applyTo(self.actual)
    assert(result is not None)
    if(self.actual == result):
      debugOhCrap = 1

    self.actual = result
    self.score = difflib.SequenceMatcher(
      None,self.actual,self.target).ratio()
    self.cost += diff.cost()

  def __str__(self):
    s = ""
    
    for step in self.steps:
      s += str(step)
      s += "\n"

    return s

  def __repr__(self):
    if len(self.steps) == 1:
      return "1 step"
    return str(len(self.steps)) + " steps"

  def applyTo(self, s):
    for step in self.steps:
      a = step.applyTo(s)
      if a is not None: s = a
    return s

  def clone(self):
    you = ChangeSequence(self.actual, self.target)
    you.start = self.start
    you.cost = self.cost
    you.steps = copy.copy(self.steps)
    return you

def AllPossibleSolutions(start, target):
  diffAlgs = copy.copy(DiffCalcs.allDiffGenerators)
  solvedSequences = []

  for a in range(20):
    # In each iteration, change the relative order of each
    # part of the diff algorithm:
    random.shuffle(diffAlgs)

    sequence = ChangeSequence(start, target)

    while True:
      anyProgress = False

      for gen in diffAlgs:
        while True:
          change = gen(sequence.actual, sequence.target)
          if change is None: 
            break

          sequence.append(change)
          anyProgress = True

      if anyProgress == False: break
    solvedSequences.append(sequence)


  solvedSequences.sort(key = lambda x : x.score /(x.cost + 1),
                       reverse = True)

  uniqueSequences = [solvedSequences[0]]

  for a, b in U.pairwise(solvedSequences):
    if a.score != b.score or a.cost != b.cost:
      uniqueSequences.append(b)

  return uniqueSequences
