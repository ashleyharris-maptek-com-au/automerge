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

    self.steps = []
   
  def append(self, diff):
    self.steps.append(diff)
    result = diff.applyTo(self.actual)
    assert(result)
    self.actual = result
    self.score = difflib.SequenceMatcher(
      None,self.actual,self.target).ratio()


def Solve(start, target):
  sequences = []
  sequences.append(ChangeSequence(start, target))

  solvedSequences = []

  while True:
    sequences.sort(key = lambda x : x.score)

    sequence = sequences.pop()

    for gen in DiffCalcs.allDiffGenerators:
      sequenceCopy = copy.copy(sequence)

      change = gen(sequenceCopy.actual, sequenceCopy.target)

      if change is None: continue

