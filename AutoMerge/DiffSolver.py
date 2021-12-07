from typing import ChainMap, Sequence
import DiffCalcs
import difflib
import copy

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
    assert(result)
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

  def applyTo(self, s):
    for step in self.steps:
      a = step.applyTo(s)
      if a is not None: s = a
    return s



def AllPossibleSolutions(start, target):
  # This algorithm is "kinda inspired" by A* - explore all open
  # paths prioritising those that appear closest to succeeding first

  sequences = []
  sequences.append(ChangeSequence(start, target))

  solvedSequences = []

  while len(sequences) > 0:
    # Find the best sequence we know of - 
    sequences.sort(key = lambda x : x.score)

    sequence = sequences.pop()

    if sequence.score == 1.0:
      solvedSequences.append(sequence)
      continue

    anyProgress = False

    for gen in DiffCalcs.allDiffGenerators:
      change = gen(sequence.actual, sequence.target)
      if change is None: 
        continue
      anyProgress = True

      sequenceCopy = copy.copy(sequence)
      sequenceCopy.append(change)

      sequences.append(sequenceCopy)

    if anyProgress == False:
      solvedSequences.append(sequence)

  solvedSequences.sort(key = lambda x : x.score /(x.cost + 1),
                       reverse = True)

  return solvedSequences
