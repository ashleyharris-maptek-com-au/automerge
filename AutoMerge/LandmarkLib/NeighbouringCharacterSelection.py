
"""

Represents a way to find a line, this may be step
one of a multi step landmark.

"""

from collections import namedtuple
import sys, inspect

try:
  from ..U import *
except:
  import os, inspect, sys
  currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  parentdir = os.path.dirname(currentdir)
  sys.path.insert(0, parentdir) 
  from U import *

class CharacterPrefix(namedtuple('CharacterPrefix',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharacterSuffix(namedtuple('CharacterSuffix',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenPrefix(namedtuple('TokenPrefix',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenSuffix(namedtuple('TokenSuffix',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class GrammarPartition(namedtuple('GrammarPartition',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharacterParition(namedtuple('CharacterParition',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenParition(namedtuple('TokenParition',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenCount(namedtuple('TokenCount',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharCount(namedtuple('CharCount',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class GrammarScopeCounter(namedtuple('GrammarScopeCounter',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class DeltaTokens(namedtuple('DeltaTokens',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class DeltaChars(namedtuple('DeltaChars',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class DeltaGrammar(namedtuple('DeltaGrammar',['impl'])):
  def Process(self, string : str, begin : int, end : int, allowRecurse = True):
    pass

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass


def FindAllCharSelectors(
  string : str, begin : int, end : int, allowRecurse = True) -> List:

  clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

  choices = []

  for cls in clsmembers:
    result = cls[1].Process(Lines, begin, end, allowRecurse)
    if result is None: continue
    if isinstance(result, list): choices.extend(result)
    else: choices.append(result)

  return choices

