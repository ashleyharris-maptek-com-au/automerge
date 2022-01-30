
"""

Represents a way to find a character (or character sequence) 
in a short section of text, this may be step
two of a multi step landmark.

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
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    prefixLength = 0

    while True:
      prefixLength += 1
      if begin - prefixLength == 0: return None
      prefix = string[begin - prefixLength : begin]

      if prefix in string[0 : begin - prefixLength]: continue
      if prefix in string[begin:]: continue

      return CharacterPrefix(prefix)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharacterSuffix(namedtuple('CharacterSuffix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    suffixLength = 0

    while True:
      suffixLength += 1
      if end + suffixLength == len(string): return None
      suffix = string[end : end + suffixLength]

      if suffix in string[0:end]: continue
      if suffix in string[end + suffixLength]: continue

      return CharacterSuffix(suffix)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenPrefix(namedtuple('TokenPrefix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    stringTokens = Tokenise(string)
    prefixTokens = Tokenise(string[0:begin])

    if stringTokens[len(prefixTokens) - 1] != prefixTokens[-1]:
      return None # We're in the middle of a token

    if stringTokens.count(prefixTokens[-1]) == 1:
      return TokenPrefix(prefixTokens[-1])

    raise NotImplementedError() # Build the longest sequence

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenSuffix(namedtuple('TokenSuffix',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    stringTokens = Tokenise(string)
    suffixTokens = Tokenise(string[end:])

    if stringTokens[0] != suffixTokens[0]:
      return None # We're in the middle of a token

    if stringTokens.count(suffixTokens[0]) == 1:
      return TokenPrefix(suffixTokens[0])

    raise NotImplementedError() # Build the longest sequence


  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class GrammarPartition(namedtuple('GrammarPartition',['before', 'mid', 'after'])):
  def ToGrammar(s :str):
    punc = re.findall(r"\W+",s.strip())
    punc = re.sub(r"\s+", "", "".join(punc))
    return punc


  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = GrammarPartition.ToGrammar(string[0:begin])
    mid = GrammarPartition.ToGrammar(string[begin:end])
    after = GrammarPartition.ToGrammar(string[end:])

    if before + after == "": return None

    return GrammarPartition(before,mid,after)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharacterParition(namedtuple('CharacterParition',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(string[0:begin])
    mid = set(string[begin:end])
    after = set(string[end:])

    beforeEx = before - mid - after
    midEx = mid - before - after
    afterEx = after - mid - before

    if beforeEx or afterEx:
      return CharacterParition(beforeEx, midEx, afterEx)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharacterPairParition(namedtuple('CharacterPairParition',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(Pairwise(string[0:begin]))
    mid = set(Pairwise(string[begin:end]))
    after = set(Pairwise(string[end:]))

    beforeEx = before - mid - after
    midEx = mid - before - after
    afterEx = after - mid - before

    if beforeEx or afterEx:
      return CharacterParition(beforeEx, midEx, afterEx)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass


class TokenParition(namedtuple('TokenParition',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = set(Tokenise(string[0:begin]))
    mid = set(Tokenise(string[begin:end]))
    after = set(Tokenise(string[end:]))

    beforeEx = before - mid - after
    midEx = mid - before - after
    afterEx = after - mid - before

    if beforeEx or afterEx:
      return TokenParition(beforeEx, midEx, afterEx)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class TokenCount(namedtuple('TokenCount',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return TokenCount(
      len(Tokenise(string[0:begin])),
      len(Tokenise(string[begin:end])),
      len(Tokenise(string[end:])))

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class CharCount(namedtuple('CharCount',['before', 'mid', 'after'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return TokenCount(
      len(string[0:begin].replace(r"\s+","")),
      len(string[begin:end].replace(r"\s+","")),
      len(string[end:].replace(r"\s+","")))

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class GrammarScopeCounter(namedtuple('GrammarScopeCounter',['before', 'mid', 'after'])):
  def ScopeCount(s : str):
    return [
      s.count('(') - s.count(')'),
      s.count('[') - s.count(']'),
      s.count('{') - s.count('}'),
      s.count('<') - s.count('>')]

  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = GrammarScopeCounter.ScopeCount(string[0:begin])
    mid = GrammarScopeCounter.ScopeCount(string[begin:end])
    after = GrammarScopeCounter.ScopeCount(string[end:])

    return GrammarScopeCounter(before, mid, after)

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class DeltaTokens(namedtuple('DeltaTokens',['token', 'beforeCount', 'midCount', 'afterCount'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = Tokenise(string[0:begin])
    mid = Tokenise(string[begin:end])
    after = Tokenise(string[end:])

    inboth = set(before).intersection(set(after))

    l = []

    for token in inboth:
      l.append(
        DeltaTokens(token, before.count(token), mid.count(token), after.count(token)))
    
    return l

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class DeltaChars(namedtuple('DeltaChars',['char','left','mid','right'])):
  def CharMap(alphabet : str, s : str):
    g = {}
    for c in alphabet: 
      if not c.isspace():
        g[c] = 0
    for c in s: 
      if not c.isspace():
        g[c] += 1
    return g

  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = string[0:begin]
    mid = string[begin:end]
    after = string[end:]

    b = DeltaChars.CharMap(string, before)
    m = DeltaChars.CharMap(string, mid)
    e = DeltaChars.CharMap(string, after)

    best = []

    for c in b.keys():
      best.append((sum([b[c], m[c], e[c]]),c,b[c], m[c], e[c]))

    best.sort(reverse=True)

    if len(best) > 4: best = best[0:4]

    results = []

    for s, c, b, m, e in best:
      results.append(DeltaChars(c, b, m, e))

    return results



  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class DeltaGrammar(namedtuple('DeltaGrammar',['before', 'mid', 'after'])):
  def ToGrammar(s :str):
    punc = re.findall(r"\W+",s.strip())
    punc = re.sub(r"\s+", "", "".join(punc))
    return punc

  def Process(string : str, begin : int, end : int, allowRecurse = True):
    before = Tokenise(string[0:begin])
    mid = Tokenise(string[begin:end])
    after = Tokenise(string[end:])

    return DeltaGrammar(before, mid, after)


  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class SelectionString(namedtuple('SelectionString',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return SelectionString(string[begin:end])

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class SelectionTokens(namedtuple('SelectionTokens',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return SelectionTokens(Tokenise(string[begin:end]))

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass

class SelectionBoundingChars(namedtuple('SelectionBoundingChars',['impl'])):
  def Process(string : str, begin : int, end : int, allowRecurse = True):
    return SelectionBoundingChars(
      string[begin - 1 : begin + 2] +
      string[end - 1 : end + 2])

  def Summary(self) -> str:
    return ""

  def Apply(self, string : str, scores : list):
    pass


def FindAllCharSelectors(
  string : str, begin : int, end : int, allowRecurse = True) -> list:

  clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

  choices = []

  for cls in clsmembers:
    result = cls[1].Process(string, begin, end, allowRecurse)
    if result is None: continue
    if isinstance(result, list): choices.extend(result)
    else: choices.append(result)

  return choices

def RunUnitTest(prefix : str, mid : str, suffix : str):
  string = prefix + mid + suffix

  selectors = FindAllCharSelectors(string, len(prefix), len(prefix) + len(mid))

  i = 0

if __name__ == '__main__':
  RunUnitTest("if (Bitrate == numN::","","Upper<Tint32u>())")