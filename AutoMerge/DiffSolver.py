from typing import ChainMap, Sequence
import DiffCalcs
import difflib
import copy
import random
import DiffCalcs.U as U

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
